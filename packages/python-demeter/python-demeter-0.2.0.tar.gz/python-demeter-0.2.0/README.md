# Demeter

Extremely limited library for downloading from and uploading files to Google Drive.

## Prerequisites

Enable the Drive API on your account and run the following:

```
pip install --upgrade oauth2client google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

You need to have your `credentials.json` file. In case this is not available, pass in your target path where it should be created and make sure to pass in a `client_secret.json`. This will open up a browser which should prompt you to authenticate and will create a `credentials.json` file afterward.

## Installing

```
pip install python-demeter
```

## Usage

```
$ credentials = <path_to_credentials.json>
$ client_secret = <path_to_client_secret.json>
$ from demeter import Demeter
$ dm = Demeter(credentials, client_secret)
$ items = dm.get_filelist()
$ for item in items:
.     print(item)
> ...
$ file_id = items[0]['id']
$ dm.download_file(file_id, 'text/csv', 'sample.csv')
$ f = dm.upload_file('sample.csv', file_path, 'txt/csv')
$ dm.give_domain_permission(f.get('id'), 'writer', 'example.com', True)
```

## License

This project is licensed under the MIT license -- see the [LICENSE](LICENSE) file for details.