import io

from oauth2client import file, client, tools
from apiclient import discovery, http

SCOPES = 'https://www.googleapis.com/auth/drive'

class Demeter(object):

    def __init__(self, credentials, client_secret):
        self.credentials = self._authorize(credentials, client_secret)
        self.service = self._build_service()
        self.files = self.service.files()
        self.permissions = self.service.permissions()

    def _authorize(self, credentials, client_secret):
        store = file.Storage(credentials)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(client_secret, SCOPES)
            credentials = tools.run_flow(flow, store)
        return credentials

    def _build_service(self):
        service = discovery.build('drive', 'v3', credentials=self.credentials)
        return service

    def get_filelist(self, page_size=100):
        fields = "nextPageToken, files(id, name)"
        results = self.files.list(pageSize=page_size, fields=fields).execute()
        items = results.get('files', [])
        if not items:
            return None
        return items

    def download_file(self, file_id, file_type, export_path):
        request = self.files.export_media(fileId=file_id, mimeType=file_type)
        fh = io.FileIO(export_path, 'wb')
        downloader = http.MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return export_path

    def upload_file(self, file_name, file_path, mime_type, team_drive=False, team_drive_id=None):
        file_metadata = {'name': file_name}
        media = http.MediaFileUpload(file_path, mimetype=mime_type)
        fl = None

        if not team_drive:
            fl = self.files.create(body=file_metadata, media_body=media, fields='id').execute()
        elif team_drive and team_drive_id is not None:
            payload = {
                'parents': [team_drive_id],
                'name': file_name
            }
            fl = self.files.create(supportsAllDrives=True, media_body=media, body=payload).execute()
        elif team_drive and team_drive_id is None:
            raise ValueError("team_drive_id should have value if this is a team drive upload")

        return fl

    def give_permission(self, file_id, permission, team_drive=False):
        pr = self.permissions.create(supportsAllDrives=team_drive, fileId=file_id, body=permission, fields='id').execute()
        return pr

    def give_domain_permission(self, file_id, role, domain, team_drive=False):
        domain_permission = {
            'type': 'domain',
            'role': role,
            'domain': domain
        }
        pr = self.give_permission(file_id, domain_permission, team_drive=team_drive)
        return pr

    def give_user_permission(self, file_id, role, email_address, team_drive=False):
        user_permission = {
            'type': 'user',
            'role': role,
            'email_address': email_address
        }
        pr = self.give_permission(file_id, user_permission, team_drive=team_drive)
        return pr
