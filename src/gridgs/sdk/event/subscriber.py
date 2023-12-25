import json
import logging
import typing
import uuid

from paho.mqtt.client import Client as PahoMqttClient, base62
from paho.mqtt.client import MQTTMessage

from gridgs.sdk.auth.client import Client as AuthClient
from .session_event import from_dict as build_session_event_from_dict, SessionEvent


def build_sessions_event_topic(company_id: int) -> str:
    return f'company/{company_id}/session_event'


class Subscriber:
    __host: str
    __port: int
    __auth_client: AuthClient
    __mqtt_client: PahoMqttClient
    __logger: logging.Logger

    def __init__(self, host: str, port: int, auth_client: AuthClient, logger: logging.Logger):
        self.__host = host
        self.__port = port
        self.__auth_client = auth_client
        self.__logger = logger
        self.__mqtt_client = PahoMqttClient('api-events-' + base62(uuid.uuid4().int, padding=22), reconnect_on_failure=True)

    def on_event(self, func: typing.Callable[[SessionEvent], None]):
        def on_message(client, userdata, msg: MQTTMessage):
            session_event_dict = json.loads(msg.payload)
            session_event = build_session_event_from_dict(session_event_dict)
            func(session_event)

        self.__mqtt_client.on_message = on_message

    def run(self):
        self.__logger.info('Grid Event Client Run')
        token = self.__auth_client.token()

        def on_connect(client, userdata, flags, rc):
            self.__logger.info('GridEventSubscriber connect')
            client.subscribe(topic=build_sessions_event_topic(token.company_id))

        self.__mqtt_client.on_connect = on_connect

        def on_disconnect(client, userdata, rc):
            self.__logger.info('GridEventSubscriber disconnect')

        self.__mqtt_client.on_disconnect = on_disconnect

        self.__mqtt_client.username_pw_set(username=token.username, password=token.access_token)
        self.__mqtt_client.connect(self.__host, self.__port)
        self.__mqtt_client.loop_forever(retry_first_connection=True)
