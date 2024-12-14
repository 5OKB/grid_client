import logging
from datetime import datetime, timedelta
from threading import Lock

from keycloak import KeycloakOpenID

from gridgs.sdk.entity import Token


class Client:
    __PRE_EXPIRATION_SECONDS = 20

    __open_id_client: KeycloakOpenID
    __username: str
    __password: str
    __company_id: int
    __token: Token = None
    __token_expires_at: datetime = datetime.min
    __refresh_token: str = ''
    __refresh_expires_at: datetime = datetime.min
    __lock: Lock
    __logger: logging.Logger

    def __init__(self, open_id_client: KeycloakOpenID, username: str, password: str, company_id: int, logger: logging.Logger):
        self.__open_id_client = open_id_client
        self.__username = username
        self.__password = password
        self.__company_id = company_id
        self.__lock = Lock()
        self.__logger = logger

    def token(self) -> Token:
        with self.__lock:
            if self.__token is None or not self.__refresh_token or datetime.now() >= self.__refresh_expires_at:
                self.__logger.info('Requesting new auth token')
                oauth_token = self.__open_id_client.token(username=self.__username, password=self.__password)
                self.__set_tokens_values(oauth_token)
            elif datetime.now() >= self.__token_expires_at:
                self.__logger.info('Refresh auth token')
                oauth_token = self.__open_id_client.refresh_token(refresh_token=self.__refresh_token)
                self.__set_tokens_values(oauth_token)

            return self.__token

    def __set_tokens_values(self, oauth_token: dict):
        self.__token = Token(username=self.__username, company_id=self.__company_id, access_token=oauth_token['access_token'])
        self.__token_expires_at = datetime.now() + timedelta(seconds=int(oauth_token['expires_in'])) - timedelta(seconds=self.__PRE_EXPIRATION_SECONDS)

        self.__refresh_token = oauth_token['refresh_token']
        self.__refresh_expires_at = datetime.now() + timedelta(seconds=int(oauth_token['refresh_expires_in'])) - timedelta(seconds=self.__PRE_EXPIRATION_SECONDS)

        self.__logger.info('Auth token', extra=_log_with_auth_token(oauth_token))


def _log_with_auth_token(value: dict) -> dict:
    if isinstance(value, dict):
        return {'oauth_expires_in': value.get('expires_in'), 'oauth_refresh_expires_at': value.get('refresh_expires_in')}
    return {}
