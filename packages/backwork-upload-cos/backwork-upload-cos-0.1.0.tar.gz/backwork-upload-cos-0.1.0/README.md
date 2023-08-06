# monsoon-upload-cos

Add support for IBM Cloud Object Storage uploads on [`monsoon`](https://github.ibm.com/apset/monsoon).

## Installing

You can use `pip` to install this plug-in directly from GHE:

```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon-upload-cos
```

Or you can use `pip` to install from Pypi repository at Artifactory

Add the following to `~/.pip/pip.conf`

```
[global]
extra-index-url = https://<email>:<api_token>@<pypi_repository_url>
```

```sh
$ pip install monsoon-upload-cos
```

## Using

After installing the plug-in you will be able to use the `upload cos`
command on `monsoon`.

```sh
$ monsoon upload cos --help
usage: monsoon upload cos [-h] [-e ENDPOINT_URL] [-s INSTANCE_ID]
                          [-u ACCESS_KEY] [-p SECRET_KEY]
                          [local_path] bucket remote_path

Upload a file to Cloud Object Storage.

positional arguments:
  local_path            path in the local file system of the file to be
                        uploaded
  bucket                target s3 bucket
  remote_path           path on Cloud Object Storage where the file will be
                        stored

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint URL of the S3 storage
  -s INSTANCE_ID, --instance-id INSTANCE_ID
                        service instance id
  -u ACCESS_KEY, --access-key ACCESS_KEY
                        acccess key id of HMAC credentials
  -p SECRET_KEY, --secret-key SECRET_KEY
                        secret access key of HMAC credentials
```

## Development

```sh
# Setup virtual environment
$ virtualenv venv --python=python3
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Install the plugin itself so you test the change
$ pip install -e .
```

## Deployment

Add the following to `.pypirc` at current project root. **DO NOT** commit this file.

```
[distutils]
index-servers = local

[local]
repository: <pypi_repository_url>
username: <email>
password: <api_token>
```

```sh
$ make publish
```

## Author

- `Michael Lin <michael.lin1@ibm.com>`
