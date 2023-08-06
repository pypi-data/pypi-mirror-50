import os
import tempfile
import dataclasses
from asyncio import CancelledError, shield
from aiohttp import web
import aiohttp_cors
from samtecdeviceshare.logger import setupLogger
from samtecdeviceshare.sdshare import SamtecDeviceShare

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BALENA_PREFIX = 'BALENA' if os.getenv('BALENA') else 'RESIN' if os.getenv('RESIN') else 'DEBUG'

logger = setupLogger('samtecdeviceshare', os.getenv('APP_LOG_PATH', tempfile.gettempdir()))
routes = web.RouteTableDef()

app = web.Application()
sds = SamtecDeviceShare()

##############################################################################
# REST Routes (v1 - legacy)
##############################################################################

@routes.get('/data.json')
async def getAppDataRequest(request):
    try:
        return web.json_response(dict(type=sds.appInfo.name, port=sds.appInfo.webPort))
    except Exception as err:
        logger.exception('Failed to get app data w/ error: %s', err)
        return web.Response(status=400, text='Failed to get app data due to error: {0}'.format(err))

@routes.get('/img.png')
async def getAppImgRequest(request):
    try:  # SDC expects this to return binary and not base64 encoded string
        return web.Response(headers={'Content-Type': 'application/octet-stream'}, status=200, body=sds.appInfo.img)
    except Exception as err:
        logger.exception('Failed to get app image w/ error: %s', err)
        return web.Response(status=400, text='Failed to get app image due to error: {0}'.format(err))

##############################################################################
# REST Routes (v2)
##############################################################################

@routes.get('/api/v2/device')
async def getDeviceStateRequest(request):
    try:
        deviceState = await sds.getDeviceState()
        return web.json_response(dataclasses.asdict(deviceState))
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to get device state w/ error:  %s', err)
        return web.Response(status=400, text='Failed to get device state w/ error: {0}'.format(err))

@routes.get('/api/v2/app')
async def getAppStateRequest(request):
    try:
        appState = await sds.getSupervisorAppState()
        return web.json_response(appState)
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to get app state w/ error:  %s', err)
        return web.Response(status=400, text='Failed to get app state w/ error: {0}'.format(err))

@routes.get('/api/v2/app/logs')
async def getAppLogsRequest(request):
    try:
        logger.info('GET /api/v2/app/logs')
        data = await sds.getLogZipData()
        return web.Response(headers={'Content-Type': 'application/octet-stream'}, status=200, body=data)
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to get app logs w/ error: %s', err)
        return web.Response(status=400, text='Failed to get app logs w/ error: {0}'.format(err))

@routes.get('/api/v2/network/wifi/credentials')
async def getWIFINetworkRequest(request):
    try:
        logger.info('GET /api/v2/network/wifi/credentials')
        return web.json_response(['unknown'])
    except Exception as err:
        logger.exception('Failed to get wifi credentials w/ error:  %s', err)
        return web.Response(status=400, text='Failed to get wifi credentials w/ error: {0}'.format(err))

@routes.post('/api/v2/device/blink')
async def performBlinkRequest(request):
    try:
        logger.info('POST /api/v2/device/blink')
        success = await sds.blinkDevice()
        return web.Response(status=200, text='Success' if success else 'Failure')
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to perform blink w/ error: %s', err)
        return web.Response(status=400, text='Failed to perform blink w/ error: {0}'.format(err))


@routes.post('/api/v2/device/restart')
async def performRestartRequest(request):
    try:
        logger.info('POST /api/v2/device/restart')
        success = await sds.restartApp()
        return web.Response(status=202, text='Success' if success else 'Failure')
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to perform restart w/ error: %s', err)
        return web.Response(status=400, text='Failed to perform restart w/ error: {0}'.format(err))


@routes.post('/api/v2/app/update/check')
async def performAppUpdateCheckRequest(request):
    try:
        logger.info('POST /api/v2/app/update/check')
        credentials = None
        try:
            credentials = await request.json()
        except Exception:
            credentials = None
        await shield(sds.performOTAUpdateCheck(credentials))
        return web.Response(status=204, text='Success')
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to perform update check w/ error: %s', err)
        return web.Response(status=400, text='Failed to perform update check w/ error: {0}'.format(err))

@routes.post('/api/v2/app/update/install')
async def performAppUpdateRequest(request):
    try:
        logger.info('POST /api/v2/app/update/install')
        success = await sds.updateApp()
        return web.Response(status=204, text='Success' if success else 'Failure')
    except (CancelledError, ConnectionResetError) as err:
        logger.exception('Request cancelled or reset (error: %s)', err)
        raise err
    except Exception as err:
        logger.exception('Failed to perform update w/ error: %s', err)
        return web.Response(status=400, text='Failed to perform update w/ error: {0}'.format(err))


@routes.post('/api/v2/network/wifi/credentials')
async def updateWIFICredentialsRequest(request):
    try:
        logger.info('POST /api/v2/network/wifi/credentials')
        credentials = await request.json()
        await sds.launchWIFIClient(
            ssid=credentials.get('ssid'),
            passphrase=credentials.get('passphrase'),
            identity=credentials.get('identity'),
            iface=credentials.get('iface')
        )
        return web.Response(status=200, text='Success')
    except Exception as err:
        logger.exception('Failed to update wifi credentials w/ error: %s', err)
        return web.Response(status=400, text='Failed to update wifi credentials w/ error: {0}'.format(err))

@routes.post('/api/v2/network/wifi/hotspot')
async def enableHotspotRequest(request):
    try:
        logger.info('POST /api/v2/network/wifi/hotspot')
        credentials = dict()
        try:
            credentials = await request.json()
        except Exception:
            credentials = dict()
        await sds.launchHotSpot(
            ssid=credentials.get('ssid'),
            passphrase=credentials.get('passphrase'),
            iface=credentials.get('iface')
        )
        return web.Response(status=200, text='Success')
    except Exception as err:
        logger.exception('Failed to enable hotspot w/ error: %s', err)
        return web.Response(status=400, text='Failed to enable hotspot w/ error: {0}'.format(err))

# Add all routes
app.add_routes(routes)

# Enable CORS for all REST/HTTP routes
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods='*'
    )
})
for route in list(app.router.routes()):
    cors.add(route)

async def startBackgroundTasks(*args):
    await sds.open()

async def cleanupBackgroundTasks(*args):
    await sds.close()

async def on_shutdown(self):
    logger.warning('Server shutting down')

if __name__ == '__main__':
    try:
        host = os.getenv('REST_ADDRESS', '0.0.0.0')
        port = int(os.getenv('REST_PORT', '47546'))
        app.on_startup.append(startBackgroundTasks)
        app.on_cleanup.append(cleanupBackgroundTasks)
        web.run_app(app, host=host, port=port, handle_signals=False)
    except KeyboardInterrupt:
        logger.warning('Exiting... due to sigkill')
    except Exception as err:
        logger.exception('Uncaught exception: %s', err)
