"""Monitor and store internet speed.


"""
from speedmonitor.speedlib import run_local_monitor, run_http_monitor
import os
import logging


LOCATION = os.environ.get('SPEEDMONITOR_LOCATION', 'unknown')
INTERVAL_SECONDS = int(os.environ.get('SPEEDMONITOR_INTERVAL_SECONDS', '60'))
FILENAME = os.environ.get('SPEEDMONITOR_FILENAME', 'speedtest.json')
HOST = os.environ.get('SPEEDMONITOR_HOST', None)
LOGLEVEL = os.environ.get('SPEEDMONITOR_LOGLEVEL', 'WARNING')

numeric_level = getattr(logging, LOGLEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(
    level=numeric_level,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
)


logger = logging.getLogger(__name__)
logger.info(
    'Config = {}'.format(
        {
            'LOCATION': LOCATION,
            'INTERVAL_SECONDS': INTERVAL_SECONDS,
            'FILENAME': FILENAME,
            'HOST': HOST
        }
    )
)



if HOST:
    logger.info('Run http monitor')
    run_http_monitor(
        HOST,
        location=LOCATION,
        interval_seconds=INTERVAL_SECONDS,
        filename=FILENAME
    )
else:
    logger.info('Run local monitor')
    run_local_monitor(
        location=LOCATION,
        interval_seconds=INTERVAL_SECONDS,
        filename=FILENAME
    )
