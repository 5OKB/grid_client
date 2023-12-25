import logging
from threading import Lock

from keycloak import KeycloakOpenID

from .token import Token


class Client:
    __open_id_client: KeycloakOpenID
    __username: str
    __password: str
    __company_id: int
    __token: Token
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
            if hasattr(self, '__token') and self.__token:  # @TODO correct condition?
                # @TODO implement refreshing
                pass
            else:
                oauth_token = self.__open_id_client.token(username=self.__username, password=self.__password)
                self.__token = Token(username=self.__username, company_id=self.__company_id, oauth_token=oauth_token)
            return self.__token
