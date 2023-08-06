# monsoon-upload-softlayer
Add support for SoftLayer uploads on [`monsoon`](https://github.ibm.com/apset/monsoon).

## Installing
You can use `pip` to install this plug-in directly from GHE:
```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon-upload-softlayer
```

## Using
After installing the plug-in you will be able to use the `upload softlayer` 
command on `monsoon`.

```sh
$ monsoon upload softlayer --help
usage: monsoon upload softlayer [-h] [-u USERNAME] [-p API_KEY]
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
