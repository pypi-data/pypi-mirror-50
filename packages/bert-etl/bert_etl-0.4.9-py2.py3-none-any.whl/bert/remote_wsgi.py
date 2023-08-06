from bert import binding, constants, utils, remote_daemon
logger.info(f'Starting service[{constants.SERVICE_NAME}] Daemon. Debug[{constants.DEBUG}]')
MIDDLEWARE = remote_daemon.setup_service()
