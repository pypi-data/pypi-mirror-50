# Speed Monitor

Monitor internet speed.

Server listens for measurements. Post speed measurements to server to persist them. Clients conduct measurements speedtest-cli and post to server.

# Get started

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
python setup.py develop
```

To start server
```
./serve.sh
```

Running tests

```
py.test
```


# Local measurements
Conducting measurements

```
SPEEDMONITOR_LOCATION='top_bedroom' SPEEDMONITOR_INTERVAL_SECONDS=60 SPEEDMONITOR_FILENAME='speedmonitor.hdf' python -m speedmonitor
```
