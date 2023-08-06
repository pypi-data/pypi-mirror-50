import requests
from requests import Session

from .errors import ApiException, NeedPasswordOrKey, AuthException


class ISPApi:
    session: Session
    password: str
    url: str
    lang: str
    session_key: str

    def __init__(self, url, username, password, lang='ru'):
        self.lang = lang
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def __del__(self):
        self.session.close()

    def _send_request(self, request_data: dict) -> requests.Response:
        response = self.session.get(url=self.url, params=request_data, verify=False)
        return response

    def send_request(self, func: str, params: dict):
        request_data = {
            'out': 'sjson',
            'func': func,
            'authinfo': f"{self.username}:{self.password}",
            'lang': 'ru',
        }
        request_data.update(params)

        response = self._send_request(request_data).json()['doc']

        if 'error' in response:
            raise ApiException(response['error']['msg']['$'])
        return response

    def get_session_key(self, username, password=None, auth_key=None):
        if not auth_key and not password:
            raise NeedPasswordOrKey()

        request_data = {
            'func': 'auth',
            'out': 'sjson',
            'username': username,
        }

        if password:
            request_data['password'] = password
        else:
            request_data['key'] = auth_key
            request_data['checkcookie'] = 'no'

        response = self._send_request(request_data).json()['doc']

        if 'error' in response:
            raise AuthException(response['error']['$object'])

        return response['auth']['$']
