import os
import glob
import tempfile
import zipfile
from dataclasses import dataclass
import asyncio
from asyncio import CancelledError, shield
from concurrent.futures import ThreadPoolExecutor
import lockfile
from lockfile import LockFile
import aiohttp
from samtecdeviceshare.helper import isOnline, getIPAddress, setupWIFIHotSpot, setupWIFIClient, awaitify, valideWPAPassphrase
from samtecdeviceshare.ethernethandler import EthernetHandler
from samtecdeviceshare.logger import setupLogger

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BALENA_PREFIX = 'BALENA' if os.getenv('BALENA') else 'RESIN' if os.getenv('RESIN') else 'DEBUG'
logger = setupLogger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))

@dataclass
class AppInfo:
    id: int = int(os.getenv(f'{BALENA_PREFIX}_APP_ID', '0'))
    name: str = os.getenv(f'{BALENA_PREFIX}_APP_NAME')
    version: str = os.getenv('APP_VERSION', '0.0.0')
    commit: str = ''
    logPath: str = os.getenv('APP_LOG_PATH', '/tmp/logs')
    webPort: int = int(os.getenv('APP_WEB_PORT', '80'))
    imgPath: str = os.getenv('APP_IMG_PATH', os.path.join(CUR_DIR, '../static/img.png'))

    img: str = b''
    status: str = 'IDLE'
    updateDownloadProgress: int = 0
    updateAvailable: bool = False
    updateDownloading: bool = False
    updateInstalling: bool = False

@dataclass
class DeviceInfo:
    id: str = os.getenv(f'{BALENA_PREFIX}_DEVICE_UUID', '0000000')
    type: str = os.getenv(f'{BALENA_PREFIX}_DEVICE_TYPE', 'raspberrypi3')
    ipAddress: str = ''

@dataclass
class DeviceState:
    status: str = 'IDLE'
    appCommit: str = ''
    appVersion: str = '0.0.0'
    appDownloadProgress: int = 0
    appUpdateAvailable: bool = False
    appDownloading: bool = False
    appUpdating: bool = False
    appUpdateCheck: bool = False
    ipAddress: str = ''
    deviceUUID: str = ''
    internetAccess: bool = False
    apMode: bool = False

@dataclass
class BalenaSupervisor:
    version: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_VERSION', '0.0.0')
    address: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_ADDRESS', 'http://localhost:48484')
    apiKey: str = os.getenv(f'{BALENA_PREFIX}_SUPERVISOR_API_KEY', '')

@dataclass
class SDCSettings:
    wifiType: str = os.getenv('SDC_WIFI_TYPE', 'HOTSPOT').upper() # HOTSPOT, CLIENT
    wifiSSID: str = os.getenv('SDC_WIFI_SSID', 'SDC-'+os.getenv(f'{BALENA_PREFIX}_DEVICE_UUID', '0000000')[:7])
    wifiPass: str = os.getenv('SDC_WIFI_PASS', 'samtec1!')
    wifiIface: str = os.getenv('SDC_WIFI_IFACE', 'wlan0')

class SamtecDeviceShare:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.loop = asyncio.get_event_loop()
        self.loop.set_default_executor(self.pool)
        self.appInfo: AppInfo = AppInfo()
        self.deviceInfo: DeviceInfo = DeviceInfo()
        self.supervisor: BalenaSupervisor = BalenaSupervisor()
        self.fetch = aiohttp.ClientSession()
        self.settings = SDCSettings()
        self.logger = logger
        lockPath = os.getenv(f'{BALENA_PREFIX}_APP_LOCK_PATH', '/tmp/balena.lock')
        if not os.path.exists(os.path.dirname(lockPath)):
            os.makedirs(os.path.dirname(lockPath))
        self.lockHandler = LockFile(os.path.splitext(lockPath)[0])
        self.ethernetHandler = EthernetHandler()
        self.internetAccess = False
        self.backgroundTask: asyncio.Task|None = None
        self.updateTask: asyncio.Task|None = None

    async def open(self) -> None:
        try:
            await self.checkInternetAccess()
            await self.setAppLock(locked=True, timeout=5)
        except Exception as err:
            self.logger.exception('Failed acquiring lock w/ error: %s', err)
        try:
            await self.launchDefaultWIFI()
        except Exception as err:
            self.logger.exception('Failed launching WiFi w/ error: %s', err)
        try:
            with open(self.appInfo.imgPath, 'rb') as fp:
                self.appInfo.img = fp.read()
        except Exception as err:
            self.logger.exception('Failed loading app image w/ error: %s', err)
        try:
            await self._updateDeviceState(force=True)
        except Exception as err:
            self.logger.exception('Failed updating device state w/ error: %s', err)
        self.backgroundTask = asyncio.create_task(self.update())

    async def close(self) -> None:
        if self.backgroundTask:
            self.backgroundTask.cancel()
            await self.backgroundTask
            self.backgroundTask = None
        if self.fetch and not self.fetch.closed:
            await self.fetch.close()
            self.fetch = None

    async def update(self) -> None:
        while True:
            try:
                for _ in range(3):
                    await asyncio.sleep(1)
                    await self._updateNetworkRoutine()
                await self._updateDeviceState()
                await self.checkInternetAccess()
            except CancelledError:
                self.logger.warning('Background task(s) cancelled')
                return
            except Exception as err:
                self.logger.exception('Failed performing update routine w/ error: %s', err)

    async def _updateNetworkRoutine(self) -> None:
        try:
            await awaitify(self.loop, self.pool, self.ethernetHandler.update)
        except (CancelledError, ConnectionResetError) as err:
            self.logger.exception('Failed updating network due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            self.logger.exception('Failed updating network w/ error: %s', err)
            raise err

    async def checkInternetAccess(self) -> bool:
        self.internetAccess = await shield(awaitify(self.loop, self.pool, isOnline))
        return self.internetAccess

    async def launchDefaultWIFI(self) -> None:
        if self.settings.wifiType == 'HOTSPOT':
            await self.launchHotSpot()
        elif self.settings.wifiType == 'CLIENT':
            await self.launchWIFIClient()
        else:
            self.logger.warning('Invalid default WIFI setup provided')

    async def launchHotSpot(self, ssid=None, passphrase=None, iface=None) -> None:
        if ssid is None and passphrase is None:
            ssid = self.settings.wifiSSID
            passphrase = self.settings.wifiPass
            iface = self.settings.wifiIface
        # Validate credentials
        if not isinstance(ssid, str):
            raise TypeError('Invalid wifi credentials: SSID missing or incorrect.')
        if not valideWPAPassphrase(passphrase):
            raise TypeError('Invalid wifi credentials: Passphrase incorrect.')
        await shield(awaitify(
            self.loop, self.pool, setupWIFIHotSpot,
            ssid=ssid, passphrase=passphrase, iface=iface,
            action='UP', timeout=20
        ))

    async def launchWIFIClient(self, ssid=None, passphrase=None, identity=None, iface=None) -> None:
        if ssid is None and passphrase is None:
            ssid = self.settings.wifiSSID
            passphrase = self.settings.wifiPass
            identity = None
        if iface is None:
            iface = self.settings.wifiIface
        # Validate credentials
        if not isinstance(ssid, str):
            raise TypeError('Invalid wifi credentials: SSID missing or incorrect.')
        if not valideWPAPassphrase(passphrase):
            raise TypeError('Invalid wifi credentials: Passphrase incorrect.')
        await shield(awaitify(
            self.loop, self.pool, setupWIFIClient,
            ssid=ssid, passphrase=passphrase, iface=iface,
            identity=identity, action='UP', timeout=20
        ))

    async def getLogZipData(self) -> bytes:
        data = await shield(awaitify(self.loop, self.pool, self._zipLogData))
        return data

    def _zipLogData(self) -> bytes:
        zipPath = os.path.join(tempfile.gettempdir(), 'app_logs.zip')
        zipfp = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
        for logFile in glob.glob(os.path.join(self.appInfo.logPath, '*.log')):
            zipfp.write(logFile, os.path.basename(logFile))
        zipfp.close()
        with open(zipPath, 'rb') as fp:
            data = fp.read()
        return data

    def setLockFile(self, lockHandler, lock, timeout=5) -> None:
        if lockHandler is None:
            raise Exception('Invalid lock handler provided')
        if lock == lockHandler.is_locked():
            self.logger.warning('Lock file already set')
            return
        try:
            lockHandler.acquire(timeout=timeout) if lock else lockHandler.release()
        except lockfile.LockError as err:
            raise err
        except lockfile.UnlockError as err:
            self.logger.warning('Forcefully breaking lock file.')
            lockHandler.break_lock()
        self.logger.info("Lock file successfully %s.", 'locked' if lock else 'unlocked')

    async def setAppLock(self, locked, timeout=5) -> None:
        if self.lockHandler:
            await shield(awaitify(
                self.loop, self.pool, self.setLockFile,
                lockHandler=self.lockHandler, lock=locked, timeout=timeout
            ))

    async def restartApp(self) -> bool:
        await self.setAppLock(locked=False)
        uri = self.supervisor.address+'/v1/reboot'
        status = 400
        async with self.fetch.post(uri, params={'apikey': self.supervisor.apiKey}) as resp:
            status = resp.status
        return status == 202

    async def updateApp(self) -> bool:
        if self.appInfo.updateInstalling:
            return True
        if self.appInfo.updateDownloading:
            raise Exception('App update still downloading')
        await self.supervisorUpdateCheck(force=False)
        if not self.appInfo.updateAvailable:
            raise Exception('No app update available')
        # Remove update lock file
        await self.setAppLock(locked=False)
        self.updateTask = asyncio.create_task(self.supervisorUpdateCheck(force=True))
        return True

    async def blinkDevice(self) -> bool:
        uri = self.supervisor.address+'/v1/blink'
        status = 400
        async with self.fetch.post(uri, params={'apikey': self.supervisor.apiKey}) as resp:
            status = resp.status
        return status == 200

    async def getDeviceState(self) -> DeviceState:
        return DeviceState(
            status=self.appInfo.status,
            appCommit=self.appInfo.commit,
            appVersion=self.appInfo.version,
            appDownloadProgress=self.appInfo.updateDownloadProgress,
            appUpdateAvailable=self.appInfo.updateAvailable,
            appDownloading=self.appInfo.updateDownloading,
            appUpdating=self.appInfo.updateInstalling,
            appUpdateCheck=self.updateTask is not None and not self.updateTask.done(),
            ipAddress=self.deviceInfo.ipAddress,
            deviceUUID=self.deviceInfo.id,
            internetAccess=self.internetAccess,
            apMode='10.42.0.1' in self.deviceInfo.ipAddress
        )

    async def getSupervisorDeviceState(self):
        uri = self.supervisor.address+'/v1/device'
        async with self.fetch.get(uri, params={'apikey': self.supervisor.apiKey}) as resp:
            devState = await resp.json()
        return devState

    async def getSupervisorAppState(self):
        uri = self.supervisor.address+'/v2/applications/state'
        async with self.fetch.get(uri, params={'apikey': self.supervisor.apiKey}) as resp:
            appState = await resp.json()
        return appState

    async def supervisorUpdateCheck(self, force=False) -> int:
        uri = self.supervisor.address+'/v1/update'
        params = {'apikey': self.supervisor.apiKey}
        body = dict(force=force)
        status = 400
        async with self.fetch.post(uri, params=params, json=body) as resp:
            status = resp.status
        return status

    async def _updateDeviceState(self, force=False) -> None:
        appCommit = self.appInfo.commit
        ifaces = [os.getenv('SDC_WIFI_IFACE', 'wlan0'), os.getenv('ETH_TARGET_NAME', 'eth0')]
        self.deviceInfo.ipAddress = ' '.join([getIPAddress(ifname) for ifname in ifaces])
        if self.internetAccess or force:
            devState = await self.getSupervisorDeviceState()
            appState = await self.getSupervisorAppState()
            appCommit = appState.get(self.appInfo.name, {}).get('commit', appCommit)
            services = [s for s in appState.get(self.appInfo.name, {}).get('services', {}).values()]
            serviceStatuses = [s.get('status', 'IDLE').upper() for s in services]

            # DOWNLOADING: At least 1 service is DOWNLOADING
            updateDownloading = 'DOWNLOADING' in serviceStatuses
            updateDownloadProgress = 0
            for service in services:
                if service.get('status', '').upper() == 'DOWNLOADING':
                    updateDownloadProgress += service.get('downloadProgress', 0) or 0
                else:
                    updateDownloadProgress += 100
            updateDownloadProgress /= max(1, len(services))
            # UPDATE AVAILABLE: At least 1 service DOWNLOADED & rest either DOWNLOADED or RUNNING
            # NOTE: RUNNING is okay- Service could have previously downloaded/installed due to no lock (power cycle)
            # NOTE: Delta may fail messing up service state: DOWNLOADING > STOPPING > STARTING > RUNNING > DOWNLOADING
            updateAvailable = 'DOWNLOADED' in serviceStatuses and all([s in ['DOWNLOADED', 'RUNNING'] for s in serviceStatuses])
            # UPDATE INSTALLING: At least 1 service INSTALLING & rest either INSTALLING, INSTALLED, STARTING, or RUNNING
            updateInstalling = 'INSTALLING' in serviceStatuses and all([s in ['INSTALLING', 'INSTALLED', 'STARTING', 'RUNNING'] for s in serviceStatuses])
            self.appInfo.updateDownloading = updateDownloading
            self.appInfo.updateDownloadProgress = updateDownloadProgress
            self.appInfo.updateAvailable = updateAvailable
            self.appInfo.updateInstalling = updateInstalling
        if not appCommit and force:
            devState = await self.getSupervisorDeviceState()
            appCommit = devState.get('commit', None)
        if appCommit is not None:
            self.appInfo.commit = appCommit

    async def performOTAUpdateTask(self) -> None:
        try:
            # Trigger supervisor to check for an update
            self.logger.info('OTA Update Check: Started')
            await self._updateDeviceState()
            await asyncio.sleep(10)
            self.logger.info('OTA Update Check: Request update')
            await self.supervisorUpdateCheck(force=False)
            await asyncio.sleep(20)
            appDownloading = True
            while appDownloading:
                self.logger.info('OTA Update Check: Waiting for potential app update to complete')
                await self._updateDeviceState()
                appDownloading = self.appInfo.updateDownloading
                await asyncio.sleep(10)
            self.logger.info('OTA Update Check: Finished')
            await self._updateDeviceState()
            await self.launchDefaultWIFI()
            return
        except Exception as err:
            self.logger.exception('OTA Update Check: Failed due to error: %s', err)
            await self.launchDefaultWIFI()

    async def performOTAUpdateCheck(self, credentials) -> None:
        try:
            if self.updateTask and not self.updateTask.done():
                return
            # Already online so just use it
            online = await self.checkInternetAccess()
            if online:
                await shield(self.supervisorUpdateCheck(force=False))
                await asyncio.sleep(1)
                return

            # Connect to supplied network
            if credentials is None:
                raise Exception('No internet access and no/invalid Wi-Fi credentials provided.')
            await self.launchWIFIClient(
                ssid=credentials.get('ssid'),
                passphrase=credentials.get('passphrase'),
                identity=credentials.get('identity'),
                iface=credentials.get('iface')
            )
            # Wait 20 seconds for internet access
            numAttempts = 0
            online = False
            while numAttempts < 20 and not online:
                await asyncio.sleep(1)
                online = await self.checkInternetAccess()
                numAttempts += 1
            if not online:
                raise Exception('Timeout reached trying to contact server.')
            # Run in seperate task
            self.updateTask = asyncio.create_task(self.performOTAUpdateTask())
            return
        except Exception as err:
            self.logger.exception('OTA Update Check: Failed due to error: %s', err)
            await self.launchDefaultWIFI()
            raise err
