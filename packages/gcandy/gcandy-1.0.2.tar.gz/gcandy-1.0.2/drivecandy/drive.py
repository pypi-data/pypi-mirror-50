"""
Wrapper for the Google Drive HTTP REST API.
"""
import jwt
import requests
import os
from .exceptions import TokenRequired, InvalidTimeToLive, \
    EnvironmentVariableNotSet, InvalidRole
from datetime import datetime, timedelta
from typing import Optional, Dict

# https://accounts.google.com/o/oauth2/v2/auth? TODO add support for standard oauth
# client_id=<>
# &redirect_uri=http://localhost:8000/
# &scope=https://www.googleapis.com/auth/drive&response_type=code

"""
Google Drive instance. Stores access token and JWT auth data.
"""


class Drive:
    def __init__(self,
                 iss: Optional[str] = None,
                 key: Optional[str] = None,
                 ):
        self.iss = iss or os.getenv('ISS')
        self.key = key or os.getenv('KEY')

        if not self.iss:
            raise EnvironmentVariableNotSet(
                'Issuer claim is needed for JSON Web Token (JWT)',
                'Set as environment variable \"ISS\" or pass as parameter')
        if not self.key:
            raise EnvironmentVariableNotSet(
                'KEY (private key) is needed for JSON Web Token (JWT)',
                'Set as environment variable \"KEY\" or pass as parameter')

        self.key = self.key.replace('\\n', '\n')
        self.base_url = 'https://www.googleapis.com/drive/v3/'
        self.access_token = None
        self.privilege_roles = ['reader',
                                'commenter',
                                'writer',
                                'fileOrganizer',
                                'organizer',
                                'owner']  # ordered low to high

        # self.get_token_personal() TODO add personal account support
        # self.get_token_service_account()
        self.get_token()

    # List[str, str, int][
    def get_token(self,
                  iss: Optional[str] = None,
                  key: Optional[str] = None,
                  ttl: Optional[int] = 60) -> str:
        """
        Requests an access token from Google by sending a JWT.

        Args:
            iss: the issuer claim identifies the principal that issued the
            JWT. The iss value is a case-sensitive string containing a
            StringOrURI value. (rfc7519 section-4.1.1)

            key: private key

            ttl: time to live in minutes, max ttl for an access token is
            60 minutes
        """
        iss = iss or self.iss
        key = key or self.key

        if not (1 <= ttl <= 60):
            raise InvalidTimeToLive(
                f'get_token({iss}, ttl={ttl})',
                'Please enter a valid ttl between '
                '1 and 60 minutes.')
        fields = {
            "iss": iss,
            "scope": "https://www.googleapis.com/auth/drive",
            "aud": "https://www.googleapis.com/oauth2/v4/token",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ttl)
        }

        encoded_jwt = jwt.encode(fields, key, algorithm='RS256')
        grant_type = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

        resp = requests.post('https://www.googleapis.com/oauth2/v4/token',
                             data={
                                 'grant_type': grant_type,
                                 'assertion': encoded_jwt
                             })

        try:
            self.access_token = resp.json()['access_token']
        except KeyError:
            print('No access token was sent.', resp.json())

        return self.access_token

    def get_files(self, fields: Optional[str] = '*') -> dict:
        url = self.build_url('files/', fields=fields)
        resp = requests.get(url)
        return resp.json(), resp.status_code

    def get_file(self, file_id: str, fields: Optional[str] = '*') -> dict:
        url = self.build_url(f'files/{file_id}', fields=fields, supportsAllDrives='True')
        resp = requests.get(url)
        return resp.json(), resp.status_code

    def get_drives(self) -> dict:
        url = self.build_url('drives/')
        resp = requests.get(url)
        return resp.json(), resp.status_code

    def get_drive_contents(self,
                           drive_id: str,fields: Optional[str] = '*') -> dict:
        # TODO document support, fix url (params will be deprecated)
        url = self.build_url('files/', driveId=drive_id, fields=fields,
                             includeItemsFromAllDrives='True', corpora='drive',
                             supportsAllDrives='True')
        resp = requests.get(url)
        return resp.json(), resp.status_code

    def get_permissions(self,
                        file_id: str, fields: Optional[str] = '*') -> dict:  # TODO test if works for drives
        url = self.build_url(f'files/{file_id}/permissions', fields=fields,
                             supportsAllDrives='True')
        resp = requests.get(url)
        return resp.json(), resp.status_code

    # def get_drive_permissions(self, drive_id: str) -> dict:
    #     url = self.build_url(f'files/{drive_id}/permissions',
    #                          supportsAllDrives='True',
    #                          )
    #     resp = requests.get(url)
    #     return resp.json()

    def get_permission(self, file_id: str, permission_id: str) -> dict:
        url = self.build_url(f'files/{file_id}/permissions/{permission_id}')
        resp = requests.get(url)
        return resp.json(), resp.status_code

    # Edit permissions ---------------------------------------------------------
    def remove_permission(self, file_id: str, permission_id: str,
                          fields: Optional[str] = '*',
                          supportsAllDrives='True') -> dict:
        """
        Args:
            file_id: id of file in question
            fields: "The paths of the fields you want included in the response.
                If not specified, the response includes a default set of fields
                specific to this method. For development you can use the special
                value '*' to return all fields, but you'll achieve greater
                performance by only selecting the fields you need."
            permission_id: id of permission to remove

        Returns:
            JSON response, if successful a "Permissions Resource"
            (https://developers.google.com/drive/api/v3/reference/permissions#resource)
        """
        url = self.build_url(f'files/{file_id}/permissions/{permission_id}',
                             fields=fields)
        resp = requests.delete(url)
        return resp.json(), resp.status_code

    def update_permission(self, file_id: str, permission_id: str,
                          new_role: str, exp_date: datetime,
                          fields: Optional[str] = '*'):
        # TODO expiration time
        """
        Args:
            file_id: id of file in question
            permission_id: id of permissions to update
            new_role: integer 1 (reader privileges) to 6 (owner privileges)
                or valid role name as a string.
            exp_date: date the new permission will expire (<1yr in the future)
            fields: "The paths of the fields you want included in the response.
                If not specified, the response includes a default set of fields
                specific to this method. For development you can use the special
                value '*' to return all fields, but you'll achieve greater
                performance by only selecting the fields you need."
        Returns:
            JSON response, if successful a "Permissions Resource"
            (https://developers.google.com/drive/api/v3/reference/permissions#resource)
        """
        url = self.build_url(f'files/{file_id}/permissions/{permission_id}',
                             fields=fields)
        try:
            if new_role in self.privilege_roles:
                role = new_role
            else:
                role = self.privilege_roles[new_role]
        except Exception:
            raise InvalidRole(f'update_permission({file_id}, {permission_id}, '
                              f'{new_role})',
                              'Enter a valid role name as a string or an int 1 '
                              '(reader privileges) to 6 (owner privileges)')
        if exp_date:
            body = {'role': role, 'expirationTime': exp_date}
        else:
            body = {'role': role}

        resp = requests.patch(url, data=body)
        return resp.json(), resp.status_code

    # Helper Functions ---------------------------------------------------------

    def build_url(self, path, **kwargs) -> str:
        try:
            access_token = kwargs.pop('access_token')
        except KeyError:
            access_token = self.access_token
        if not access_token:  # self.access token has not been set
            exp = f'build_url(path={path}, access_token=self.access_token)'
            msg = 'No access_token. Get an access token by calling getToken()' \
                  ' or provide one as a parameter.'
            raise TokenRequired(exp, msg)
        # Parse kwargs
        if len(kwargs) != 0:
            args = '&'.join("{!s}={!s}".format(key, val)
                            for (key, val) in kwargs.items())
            return f'{self.base_url}{path}?access_token={access_token}&{args}'

        return f'{self.base_url}{path}?access_token={access_token}'
