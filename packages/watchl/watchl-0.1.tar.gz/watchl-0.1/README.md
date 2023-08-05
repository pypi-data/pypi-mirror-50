# watchl

[![build status](https://travis-ci.com/florimondmanca/watchl.svg?token=2WTbCxyyjrjzR5LpHFc3&branch=master)](https://travis-ci.com/florimondmanca/watchl)
[![codecov](https://codecov.io/gh/florimondmanca/watchl/branch/master/graph/badge.svg?token=O5ZSL569hc)](https://codecov.io/gh/florimondmanca/watchl)
[![code style](https://img.shields.io/badge/code_style-black-black)](https://github.com/psf/black)
![license](https://img.shields.io/badge/license-MIT-green)

Lightweight HTTP log monitoring and alerting console tool written in Python.

**Note**: only [W3C-formatted logs](https://www.w3.org/Daemon/User/Config/Logging.html) are supported for now. See [here](https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs) for an example W3C-formatted log file.

## Features

- Live tail of log files.
- Stats reporting in the console: top hit sections, traffic, throughput, etc.
- Live alerting and recovery detection with customizable thresholds and delays.
- Friendly command line interface.
- Detailed and machine-readable JSON-formatted output.
- Asynchronous architecture with low resources footprint.
- Optional Docker-based execution.

Example command:

```
$ watchl -f access.log --report-every=2 --alert-tick=2 --traffic-up=1 --traffic-down=1
```

Output (JSON prettification by piping into [jq](https://stedolan.github.io/jq/)):

```json
{
  "levelname": "INFO",
  "message": "process started",
  "timestamp": "2019-07-30T21:02:30.652107",
  "pid": 2417
}
{
  "levelname": "INFO",
  "message": "watching logs",
  "timestamp": "2019-07-30T21:02:30.653034",
  "path": "access.log"
}
{
  "levelname": "INFO",
  "message": "activity in the past 2.0 seconds",
  "timestamp": "2019-07-30T21:02:32.708673",
  "sections.count": {
    "unit": "hits",
    "value": [
      {
        "key": "/presentations",
        "count": 68
      },
      {
        "key": "/images",
        "count": 13
      },
      {
        "key": "/blog",
        "count": 9
      }
    ]
  },
  "requests.total": {
    "unit": "req",
    "value": 135
  },
  "requests.average": {
    "unit": "req/s",
    "value": 67.5
  },
  "transfer.average": {
    "unit": "bytes/s",
    "value": 3064559
  },
  "transfer.mean": {
    "unit": "bytes/req",
    "value": 45400.874074074076
  }
}
{
  "levelname": "WARNING",
  "message": "alert status changed",
  "timestamp": "2019-07-30T21:02:34.773988",
  "status": "active",
  "previous_status": "activating",
  "value": 89.5,
  "reason": "stayed above threshold for longer than up delay",
  "metric": "requests.average",
  "threshold": 10,
  "up": "0:00:01",
  "down": "0:00:01"
}
...
```

## Installation

- If you have Python 3.6+ installed, you can install `watchl` from PyPI:

```bash
pip install watchl
```

or locally by cloning the repository and running:

```bash
pip install .
```

- If you have Docker installed, you can build the image using:

```bash
docker build -t watchl .
```

## Usage

### General notes

`watchl` exposes a command line executable named `watchl`.

When run without any other options, `watchl` will read logs from `/tmp/access.log` (this is configurable — see [CLI reference](#cli-reference) for options) and consume them as they are written to the file.

> **Known limitation**: `watchl` does not handle log rotation yet. If the log file is renamed, truncated or moved, `watchl` won't be able to read new logs anymore, and will need to be restarted. See [#9](https://github.com/florimondmanca/watchl/issues/9).

If you are using Docker, and assuming you have a log file somewhere on your machine, you can run a `watchl` container using:

```
docker run -it --rm -v /host/path/to/access.log:/tmp/access.log watchl <options>
```

By default, `watchl` works on relatively long time scales (minutes). For quicker feedback (e.g. when trying `watchl` for the first time), you can try the following options:

```bash
watchl --report-every=5 --alert-tick=1 --traffic-up=1 --traffic-down=1
```

### CLI reference

```
Usage: watchl [OPTIONS]

Options:
  -f PATH                         Path to an actively written-to log file.
                                  [default: /tmp/access.log]
  --report-every FLOAT            Number of seconds between stats reports.
                                  [default: 10]
  --sections-top INTEGER          Number of most hit website sections to
                                  display in the report.  [default: 3]
  --traffic-threshold FLOAT       [default: 10]
  --traffic-up FLOAT              Number of seconds to trigger an alert after
                                  traffic exceeded the threshold.  [default:
                                  120]
  --traffic-down FLOAT            Number of seconds to stop an alert after
                                  traffic dropped below the threshold.
                                  [default: 120]
  --alert-tick FLOAT              Number of seconds between evaluation of
                                  stats for alerting purposes.  [default: 10]
  --tick FLOAT                    Number of seconds between system event
                                  checks. Note: lower values increase CPU
                                  usage.  [default: 0.5]
  --log-level [debug|info|warning|critical|error]
                                  Level for internal log messages  [default:
                                  info]
  --limit-max-log-lines INTEGER   Limit the number of log lines to ingest
                                  before terminating the process.
  --help                          Show this message and exit.
```

## Contributing

See [Contributing guidelines](https://github.com/florimondmanca/watchl/blob/master/CONTRIBUTING.md).

## License

MIT
