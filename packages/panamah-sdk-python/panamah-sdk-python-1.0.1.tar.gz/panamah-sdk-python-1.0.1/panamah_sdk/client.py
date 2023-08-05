import requests
import time
import base64
import hashlib
from .exceptions import AuthException, RefreshException
from os import environ

GLOBAL_BASE_URL =  environ.get('PANAMAH_API_URL') if environ.get('PANAMAH_API_URL') else 'https://panamah.io/api/v2'
GLOBAL_SDK_IDENTITY = "panamah-python1.0.0"


class Client():
    """Base HTTP client for admin and stream"""

    def make_request(self, method, url, payload, headers):
        path = '/' + url if not url.startswith('/') else url
        url_with_path = GLOBAL_BASE_URL + path
        identified_headers = {
            **headers,
            ** {'x-sdk-identity': GLOBAL_SDK_IDENTITY}
        } if headers else {'x-sdk-identity': GLOBAL_SDK_IDENTITY}
        response = requests.request(
            method=method,
            url=url_with_path,
            json=payload,
            headers=identified_headers
        )
        return response

    def post(self, url, payload, headers={}):
        return self.make_request(
            "POST",
            url,
            payload,
            headers=headers
        )

    def put(self, url, payload, headers={}):
        return self.make_request(
            "PUT",
            url,
            payload,
            headers
        )

    def delete(self, url, payload, headers={}):
        return self.make_request(
            "DELETE",
            url,
            payload,
            headers
        )

    def get(self, url, headers={}):
        return self.make_request(
            "GET",
            url,
            None,
            headers
        )


class AdminClient(Client):

    def __init__(self, authorization_token=None):
        self.authorization_token = authorization_token

    def make_request(self, method, url, payload, headers):
        return super().make_request(
            method,
            url,
            payload,
            {
                **headers,
                **{"Authorization": self.authorization_token}
            }
        )


class StreamClient(Client):

    def __init__(self, authorization_token=None, secret=None, assinante_id='*'):
        self.authorization_token = authorization_token
        self.secret = secret
        self.assinante_id = assinante_id
        self._tokens = None

    def authenticate(self, authorization_token, secret, assinante_id):
        timestamp = int(time.time())
        payload = {
            "assinanteId": assinante_id,
            "key": self.calculate_key(
                secret,
                assinante_id,
                timestamp
            ),
            "ts": timestamp
        }
        response = super().make_request(
            method='POST',
            url='/stream/auth',
            payload=payload,
            headers={
                "Authorization": authorization_token
            }
        )
        if response.status_code == 200:
            return response.json() if response.content else None
        elif response.status_code == 403:
            raise AuthException("Credenciais invalidas")
        else:
            raise AuthException("Erro nao esperado: %d" % response.status_code)

    def refresh_tokens(self, refresh_token):
        response = super().make_request(
            method='GET',
            url='/stream/auth/refresh',
            payload=None,
            headers={
                "Authorization": refresh_token
            }
        )
        if response.status_code == 200:
            return response.json() if response.content else None
        else:
            raise RefreshException(
                "Erro no refresh do token: %d" % response.status_code)

    def calculate_key(self, secret, assinante_id, timestamp):
        return base64.b64encode(hashlib.sha1((secret + assinante_id + str(timestamp)).encode('utf-8')).digest()).decode('utf-8')

    def make_authenticated_request(self, method, url, payload, headers):
        response = super().make_request(
            method,
            url,
            payload,
            {
                **headers,
                **{
                    "Authorization": self._tokens["accessToken"]
                }
            }
        )
        if response.status_code == 403:
            self._tokens = self.refresh_tokens(self._tokens['refreshToken'])
            response = super().make_request(
                method,
                url,
                payload,
                {
                    **headers,
                    **{
                        "Authorization": self._tokens["accessToken"]
                    }
                }
            )
        return response

    def make_request(self, method, url, payload, headers):
        if not self._tokens:
            self._tokens = self.authenticate(
                self.authorization_token, self.secret, self.assinante_id)
        return self.make_authenticated_request(method, url, payload, headers)
