"""Library for running, storing and reading speed tests.

Classes
-------
SpeedMonitor:
   Cooperative base class implementing business logic of running
   an internet speed measurement once or continuously. Must be
   combined with a mixin Storage class implementing `store_speed` and
   `read_speed` methods.

LocalFileStorage:
   A storage mixin class implementing `store_speed` and `read_speeds`
   to a local hdf5 file. Should be combined with a SpeedMonitor class.

HTTPFileStorage:
   A remote mixin class implementing `store_speed` and `read_speeds`
   by interacting with an http server. Should be combined with a
   SpeedMonitor class.

LocalSpeedMonitor:
   Can be used to run internet speed measurements and store them in a
   local file.

HTTPSpeedMonitor:
   Can be used to run internet speed measurements and publish them to
   an http server.


Examples
--------

Initializing a local speed monitor

>>> from speedmonitor.speedlib import LocalSpeedMonitor
>>> monitor = LocalSpeedMonitor(filename='speedmeasurements.hdf', location='doctest', interval_seconds=20)

Use `run` to run measurements every `interval_seconds`. Include
`limit` parameter to limit the number of measurements.

>>> monitor.run(2)
{'download': 2511286.369176327, 'upload': 1425310.47277141, 'ping': 17.827, 'timestamp': '2019-08-11T05:26:55.587998Z', 'bytes_sent': 2629632, 'bytes_received': 3856320, 'share': None, 'location': 'doctest'}
{'download': 366144.2295192711, 'upload': 601656.44654631, 'ping': 105.978, 'timestamp': '2019-08-11T05:27:57.128886Z', 'bytes_sent': 1441792, 'bytes_received': 665600, 'share': None, 'location': 'doctest'}

The monitor also behaves like a Python generator. To run a single measurement:

>>> next(monitor)
{'download': 3939993.670846969, 'upload': 2589204.369534852, 'ping': 18.843, 'timestamp': '2019-08-11T05:13:19.603453Z', 'bytes_sent': 3481600, 'bytes_received': 8837696, 'share': None, 'location': 'doctest'}

To measure the speed manually

>>> speed = monitor.measure_speed()
>>> speed
{'download': 73649.56504261198, 'upload': 404321.2157027885, 'ping': 610.814, 'timestamp': '2019-08-10T16:51:58.050413Z', 'bytes_sent': 868352, 'bytes_received': 133120, 'share': None, 'location': 'doctest'}

To store a speed measurement manually
>>> stored = monitor.store_speed(speed)
>>> stored
{'download': 6585057.816690687, 'upload': 5705400.29055425, 'ping': 25.172, 'timestamp': '2019-08-11T05:10:23.119700Z', 'bytes_sent': 7200768, 'bytes_received': 8559364, 'share': None, 'location': 'doctest'}
>>> stored == speed
True

""" # noqa
from itertools import islice
from speedmonitor import speedtest
import os
import json
from requests.compat import urljoin
import requests
import logging


logger = logging.getLogger(__name__)


##################################################
# measuring internet speed
##################################################
def measure_speed(location, threads=4):
    servers = []
    spt = speedtest.Speedtest()
    spt.get_servers(servers)
    spt.get_best_server()
    spt.download(threads=threads)
    spt.upload(threads=threads)
    res = spt.results.dict()
    res['location'] = location
    return {k: v for (k, v) in res.items() if k not in {'server', 'client'}}


##################################################
# io
##################################################
class SpeedMonitor:

    def __init__(self,  *args, location='unknown', threads=4,
                 interval_seconds=60, **kwargs):
        self.location = location
        self.threads = threads
        self.interval_seconds = interval_seconds
        super().__init__(*args, **kwargs)

    def measure_speed(self):
        speed = measure_speed(self.location, self.threads)
        return speed

    def __iter__(self):
        return self

    def __next__(self):
        speed = self.measure_speed()
        response = self.store_speed(speed=speed)
        return response

    def run(self, limit=None):
        for speed in islice(self, limit):
            print(speed)
            try:
                speed = next(self)
            except Exception:
                logger.exception('Exception raised attempting '
                                 'to measure and store speed.')

    def store_speed(self, *args, **kwargs):
        return super().store_speed(*args, **kwargs)

    def read_speeds(self, *args, **kwargs):
        return super().read_speeds(*args, **kwargs)

    def encode_speed(self, *args, **kwargs):
        return super().encode_speed(*args, **kwargs)

    def decode_speed(self, *args, **kwargs):
        return super().decode_speed(*args, **kwargs)


class JSONFileStorage:

    SEPARATORS = (',', ':')

    def __init__(self, filename='speedtest.json', **kwargs):
        self.filename = filename

    def read_speeds(self):
        with open(self.filename, 'r', encoding='utf-8') as fid:
            for line in fid:
                yield json.loads(line)

    def store_speed(self, speed=None):
        if speed is None:
            return None
        serialized = self.encode_speed(speed=speed)
        with open(self.filename, 'a+', encoding='utf-8') as fid:
            fid.write(serialized)
            fid.write('\n')
        return self.decode_speed(speed=serialized)

    def encode_speed(self, speed=None):
        if speed is None:
            return '{}'
        # don't just use json.dumps because
        # it doesn't work for numpy
        return json.dumps(speed, separators=self.SEPARATORS)

    def decode_speed(self, speed=None):
        if speed is None:
            return {}
        return json.loads(speed)


class HTTPFileStorage:

    def __init__(self, base_url, filename='speedtest.json', key='speedtest'):
        self.filename = filename
        self.key = key
        self.base_url = base_url
        self.post_queue = []

    def read_speeds(self):
        url = urljoin(self.base_url, '/api/speedtests')
        response = requests.get(url, json={
            'filename': self.filename,
        })
        if response.ok:
            for line in response.json()['speeds']:
                yield json.loads(line)

    def store_speed(self, speed=None):

        res = self._store(speed)

        if res is not None:
            # we've got connectivity so let's try emptying the queue
            for queued_speed in self.post_queue:
                stored = self._store(queued_speed)
                logger.info(f'{stored} stored from queue')

        return res

    def _store(self, speed=None):
        if speed is None:
            return None
        url = urljoin(self.base_url, '/api/speedtests')
        try:
            response = requests.post(url, json={
                'speed': speed,
                'filename': self.filename,
            })
        except Exception:
            logger.error(f'Failed to post speed {speed} to {url}. Adding to queue.')
            self.post_queue.append(speed)
            logger.info('Length of post queue = {}'.format(len(self.post_queue)))
            return
        if response.ok:
            output_speed = response.json()['speed']
            logger.info(f'stored speed {output_speed}')
            return output_speed

        return response.json()


class JSONSpeedMonitor(SpeedMonitor, JSONFileStorage):
    pass


class HTTPSpeedMonitor(SpeedMonitor, HTTPFileStorage):
    pass


LocalFileStorage = JSONFileStorage
LocalSpeedMonitor = JSONSpeedMonitor


##################################################
# scripting layer
##################################################
def run_local_monitor(location='unknown',
                      interval_seconds=60,
                      filename='speedtest.json'):
    monitor = JSONSpeedMonitor(
        location=location,
        interval_seconds=interval_seconds,
        filename=filename
    )
    monitor.run()


def run_http_monitor(base_url,
                     location='unknown',
                     interval_seconds=60,
                     filename='speedtest.json'):
    monitor = HTTPSpeedMonitor(
        base_url,
        location=location,
        interval_seconds=interval_seconds,
        filename=filename
    )
    monitor.run()
