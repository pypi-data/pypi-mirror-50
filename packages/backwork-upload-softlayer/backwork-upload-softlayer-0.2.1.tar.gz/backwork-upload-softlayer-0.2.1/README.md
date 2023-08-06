# backwork-upload-softlayer [![Build Status](https://travis-ci.org/IBM/backwork-upload-softlayer.svg?branch=master)](https://travis-ci.org/IBM/backwork-upload-softlayer) [![PyPI version](https://badge.fury.io/py/backwork-upload-softlayer.svg)](https://badge.fury.io/py/backwork-upload-softlayer)
Add support for SoftLayer uploads on [`backwork`](https://github.com/IBM/backwork).

## Installing
You can use `pip` to install this plug-in:
```sh
$ pip install backwork-upload-softlayer
```

## Using
After installing the plug-in you will be able to use the `upload softlayer`
command on `backwork`.

```sh
$ backwork upload softlayer --help
usage: backwork upload softlayer [-h] [-u USERNAME] [-p API_KEY]
                                [-d DATACENTER] [-c CONTAINER]
                                [local_path] remote_path

Upload a file to Softlayer ObjectStorage.

positional arguments:
  local_path            path in the local file system of the file to be
                        uploaded
  remote_path           path on Softlayer ObjectStorage container where the
                        file will be stored

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username for Softlayer ObjectStorage API
  -p API_KEY, --api-key API_KEY
                        api key for Softlayer ObjectStorage API
  -d DATACENTER, --datacenter DATACENTER
                        datacenter where the file will be stored
  -c CONTAINER, --container CONTAINER
                        target container
```
