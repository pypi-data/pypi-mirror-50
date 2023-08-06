import logging
logger = logging.getLogger(__name__)
from bert import constants, remote_webservice
logger.info(f'Starting service[{constants.SERVICE_NAME}] Daemon. Debug[{constants.DEBUG}]')
MIDDLEWARE = remote_webservice.setup_service()
