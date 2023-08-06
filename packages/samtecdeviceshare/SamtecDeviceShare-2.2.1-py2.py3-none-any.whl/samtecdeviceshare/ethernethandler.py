""" Ethernet Handler """
#!/usr/bin/env python
import os
import time
import tempfile
from samtecdeviceshare.logger import setupLogger

logger = setupLogger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))

if os.getenv('PYTHON_ENV') != 'development':
    import NetworkManager as NM
else:
    logger.warning('Using NetworkManager emulator in development mode.')
    class NetworkManager:
        NM_DEVICE_STATE_ACTIVATED = 100
        NM_DEVICE_STATE_IP_CHECK = 80
        NM_DEVICE_STATE_IP_CONFIG = 70
        NM_DEVICE_STATE_FAILED = 120
        NM_DEVICE_STATE_UNAVAILABLE = 20
        NM_DEVICE_STATE_UNMANAGED = 10
        NM_DEVICE_TYPE_ETHERNET = 1
        def __init__(self):
            pass
        def nm_state(self):
            pass
    NM = NetworkManager

class EthernetHandler:
    CONN_STATES = ['DISCONNECTED', 'CONNECTING', 'CONNECTED']
    NM_CONNECTED_STATES = [NM.NM_DEVICE_STATE_ACTIVATED]
    NM_CONNECTING_STATES = [
        NM.NM_DEVICE_STATE_IP_CHECK,
        NM.NM_DEVICE_STATE_IP_CONFIG
    ]
    NM_DISCONNECTED_STATES = [
        NM.NM_DEVICE_STATE_FAILED,
        NM.NM_DEVICE_STATE_UNAVAILABLE,
        NM.NM_DEVICE_STATE_UNMANAGED
    ]

    def __init__(self, targetDevName=None):
        self.DHCP_TIMEOUT = int(os.getenv('ETH_DHCP_TIMEOUT', '15'))
        self.LINK_LOCAL_TIMEOUT = int(os.getenv('ETH_LOCAL_TIMEOUT', '30'))
        self.targetDevName = targetDevName or os.getenv('ETH_TARGET_NAME')
        self.REFRESH_DELAY = 1
        self.devName = None
        self.devState = None
        self.conName = None
        self.conState = 'DISCONNECTED'
        self.conCounter = 0
        self.conNeedsInit = True

    def run(self):
        while True:
            try:
                time.sleep(self.REFRESH_DELAY)
                self.update()
            except Exception as err:
                logger.exception('Received following exception: %s', err)

    def getWiredDevice(self):
        for dev in NM.NetworkManager.GetDevices():
            isEthernet = dev.DeviceType == NM.NM_DEVICE_TYPE_ETHERNET
            isTargetDevice = not self.targetDevName or (self.targetDevName and self.targetDevName == dev.Interface)
            if isEthernet and isTargetDevice:
                return dev
        return None

    def getActiveWiredConnection(self):
        for act in NM.NetworkManager.ActiveConnections:
            try:
                settings = act.Connection.GetSettings()
                actDevs = [d for d in act.Devices]
                # Skip if connection isnt 802-3-ethernet or no devices attached
                if settings['connection'].get('type') != '802-3-ethernet' or\
                   '802-3-ethernet' not in settings or not actDevs:
                    continue
                # If no target specified, pick first dev
                if not self.targetDevName:
                    return act.Connection, actDevs[0]
                # Otherwise, find target device
                foundDev = next((d for d in actDevs if d.Interface == self.targetDevName), None)
                if foundDev:
                    return act.Connection, foundDev
            except Exception as err:
                logger.warning('Skipping active connection. Failed parsing with error: %s', err)
        return None, None

    def updateActiveWiredConnection(self, con=None, dev=None, method='auto'):
        success = False
        try:
            settings = con.GetSettings()
            # Add IPv4 setting if it doesn't yet exist
            if 'ipv4' not in settings:
                settings['ipv4'] = {}
            # Set the method and change properties
            settings['ipv4']['method'] = method
            settings['ipv4']['addresses'] = []
            con.Update(settings)
            con.Save()
            NM.NetworkManager.ActivateConnection(con, dev, "/")
            success = True
        except Exception:
            success = False
        return success

    def update(self):
        if os.environ.get('PYTHON_ENV') == 'development':
            return
        # Disable this feature (e.g pi zero)
        if os.getenv('ETH_DISABLE'):
            return
        nextConName = None
        nextDevName = None
        nextDevState = None
        nextConMethod = None
        nextConState = None
        con, dev = self.getActiveWiredConnection()

        # Get device and connection name and state
        if con is None or dev is None:
            self.conNeedsInit = True
            dev = self.getWiredDevice()
            conSettings = None
            conMethod = 'auto'
            nextConName = 'Unknown'
            nextDevName = dev.Interface if dev else None
            nextDevState = dev.State if dev else NM.NM_DEVICE_STATE_UNAVAILABLE
        else:
            conSettings = con.GetSettings()
            conMethod = conSettings.get('ipv4', {}).get('method', '')
            nextConName = conSettings.get('connection', {}).get('id', '')
            nextDevName = dev.Interface
            nextDevState = dev.State

        # Determine whether to change connection method
        if nextDevState in EthernetHandler.NM_CONNECTED_STATES:
            self.conCounter = 0
            nextConState = 'CONNECTED'
            nextConMethod = conMethod
        elif nextDevState in EthernetHandler.NM_CONNECTING_STATES:
            nextConState = 'CONNECTING'
            # DHCP timeout, go to Link-Local
            if conMethod == 'auto' and self.conCounter >= self.DHCP_TIMEOUT:
                logger.info('auto method timeout. Switching to link-local')
                nextConMethod = 'link-local'
                self.conCounter = 0
            # Link-Local timeout, go to DHCP
            elif conMethod == 'link-local' and self.conCounter >= self.LINK_LOCAL_TIMEOUT:
                logger.info('link-local method timeout. Switching to auto')
                nextConMethod = 'auto'
                self.conCounter = 0
            else:
                nextConMethod = conMethod
                self.conCounter += 1

        elif nextDevState in EthernetHandler.NM_DISCONNECTED_STATES:
            self.conCounter = 0
            nextConState = 'DISCONNECTED'
            nextConMethod = 'auto'
        else:
            self.conCounter = self.conCounter
            nextConState = nextConState
            nextConMethod = conMethod

        if nextDevName != self.devName:
            logger.info('Wired device name changed to {0}'.format(nextDevName))
        if nextConName != self.conName:
            logger.info('Wired connection name changed to {0}'.format(nextConName))
        if nextConState != self.conState:
            logger.info('Wired connection state changed to {0}'.format(nextConState))

        # If have connection and want method to change or needs initialization
        if con and (self.conNeedsInit or (nextConMethod != conMethod)):
            # IMPORTANT: On init we must start with DHCP
            nextConMethod = 'auto' if self.conNeedsInit else nextConMethod
            logger.info('Setting connection {0} to method {1}'.format(nextConName, nextConMethod))
            success = self.updateActiveWiredConnection(con, dev, nextConMethod)
            # NOTE: If failed to activate, we'll retry next iteration
            if not success:
                nextConMethod = conMethod
                self.conNeedsInit = True
                logger.error('Failed setting active connection method.')
            else:
                self.conNeedsInit = False
                logger.info('Successfully set active connection method.')
        self.devName = nextDevName
        self.devState = nextDevState
        self.conName = nextConName
        self.conState = nextConState

if __name__ == '__main__':
    handler = EthernetHandler()
    handler.run()
