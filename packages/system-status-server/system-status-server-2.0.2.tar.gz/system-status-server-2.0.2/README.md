[![Build Status](https://travis-ci.org/voidpp/system-status-server.svg?branch=master)](https://travis-ci.org/voidpp/system-status-server)
[![Coverage Status](https://coveralls.io/repos/github/voidpp/system-status-server/badge.svg?branch=master)](https://coveralls.io/github/voidpp/system-status-server?branch=master)

About
--

Microservice to get some system status info in JSON.

Available nodes:
--

- Uptime
- Load
- CPU (number of cores)
- Memory usage
- HDD

Installation:
--
`pip install system-status-server`

Usage
--
CLI for hdd stat:
```bash
hdd-stat
```

uWSGI example config:
```ini
[uwsgi]
processes = 2
module = system_status_server.app:app
http-socket = :35280
```

Typical output:
--
```json
{
	"load": [0.29, 0.33, 0.27],
	"hdd": [
		{
			"device": "/dev/mmcblk0p2",
			"free": 946810880,
			"label": "trusty",
			"mount": "/",
			"percent": 83.0,
			"total": 7425466368,
			"used": 6165794816
		},
		{
			"device": "/dev/mmcblk0p1",
			"free": 122949632,
			"label": "BOOT",
			"mount": "/boot",
			"percent": 8.6,
			"total": 134582272,
			"used": 11632640
		}
	],
	"uptime": 3403979,
	"cpu": {
		"cores": 8
	},
	"memory": {
		"available": 13979320320,
		"total": 16503238656,
		"percent": 15.3,
		"free": 2553470976,
		"used": 13949767680
	}
}
```
