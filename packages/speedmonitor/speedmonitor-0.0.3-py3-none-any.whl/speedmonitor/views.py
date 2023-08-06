"""Listen for requests to store speedtest measurements.
"""
import logging

from speedmonitor.speedlib import LocalFileStorage

from flask import Flask, jsonify, request, Blueprint

logger = logging.getLogger(__name__)
blueprint = Blueprint('speedtest', __name__)

DEFAULT_FILENAME = 'speedtest.json'
DEFAULT_KEY = 'speedtest'


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    logging.basicConfig(level=logging.DEBUG, filename='speedtest.log')
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())
    return app


@blueprint.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ok',
        'version': '0.01'
    })


@blueprint.route('/api/speedtests', methods=['GET', 'POST'])
def speedtests():
    logger.info('request method = %s' % request.method)

    if request.method == 'GET':
        filename = request.json.get('filename', None) or DEFAULT_FILENAME
        key = request.json.get('key', None) or DEFAULT_KEY
        storage = LocalFileStorage(filename=filename, key=key)
        speeds = storage.read_speeds()
        encoded_speeds = [storage.encode_speed(speed=x) for x in speeds]
        output = jsonify({
            'speeds': encoded_speeds
        })
        logger.debug(
            'GET request: reading `speeds` from `filename`'
            'and returning `output`\n{}'.format({
                'filename': f'{filename}',
                'speeds': f'{speeds}',
                'output': f'{output}'
            })
        )
        return output

    if request.method == 'POST':
        data = request.json
        speed = data.get('speed')
        filename = data.get('filename')
        key = data.get('key')
        logger.debug('POST request: entering with params {}'.format(
            {
                'filename': filename,
                'key': key,
                'speed': speed
            }
        ))
        storage = LocalFileStorage(filename=filename, key=key)
        error = None
        try:
            speed_dict = storage.store_speed(speed)
        except Exception as err:
            logger.exception('Unable to store speed f{speed}')
            error = str(err)

        output = jsonify({
            'speed': storage.encode_speed(speed=speed_dict),
            'error': error
        })
        logger.debug(f'POST request: returning output={output!r}')
        return output
