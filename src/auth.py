import pickle
import os.path
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Auth:

    def __init__(self, this_directory, SCOPES):
        self.this_directory = this_directory
        self.SCOPES = SCOPES

    def get_config_from_file(self, file_path):
        data = ""
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    def add_envars_config(self, config):
        CLIENTID = os.getenv('CLIENTID')
        PROJECTID = os.getenv('PROJECTID')
        CLIENTSECRET = os.getenv('CLIENTSECRET')
        update_vals = {
            "client_id": CLIENTID,
            "project_id": PROJECTID,
            "client_secret": CLIENTSECRET
            }
        config['installed'].update(update_vals)

        return config

    def get_credentials(self):
        creds = None
        # token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization
        # flow completes for the first
        # time
        secrets_path = os.path.join(self.this_directory, 'externals')
        token_path = os.path.join(secrets_path, 'token.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # if there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                secrets_file = os.path.join(secrets_path, 'googledrive.json')
                config_from_file = self.get_config_from_file(secrets_file)
                config_from_file = self.add_envars_config(config_from_file)
                flow = InstalledAppFlow.from_client_config(
                        config_from_file,
                        self.SCOPES
                    )
                creds = flow.run_local_server(port=8000)
            # save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds
