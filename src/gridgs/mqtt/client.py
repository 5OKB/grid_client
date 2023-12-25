import json
import logging
import uuid
from typing import Callable

from paho.mqtt.client import Client as PahoMqttClient, MQTTMessageInfo, MQTTMessage, base62

from application.grid.auth.client import Client as AuthClient
from application.grid.entity.frame import Frame, frame_from_dict
from application.grid.entity.session import Session
from application.grid.mqtt.interface import Connector, Subscriber, Sender


def build_downlink_topic(session: Session) -> str:
    return f'satellite/{session.satellite.id}/downlink/gs/{session.ground_station.id}'


def build_uplink_topic(session: Session) -> str:
    return f'satellite/{session.satellite.id}/uplink/gs/{session.ground_station.id}'


class Client(Connector, Subscriber, Sender):
    __host: str
    __port: int
    __auth_client: AuthClient
    __mqtt_client: PahoMqttClient
    __logger: logging.Logger

    def __init__(self, host: str, port: int, auth_client: AuthClient, logger: logging.Logger):
        self.__host = host
        self.__port = port
        self.__auth_client = auth_client
        self.__mqtt_client = PahoMqttClient('api-frames-' + base62(uuid.uuid4().int, padding=22), reconnect_on_failure=True)
        self.__logger = logger

    def connect(self) -> None:
        self.__logger.info('GRID MQTT Client connecting')
        token = self.__auth_client.token()
        self.__mqtt_client.username_pw_set(username=token.username, password=token.access_token)
        self.__mqtt_client.connect(self.__host, self.__port)
        self.__mqtt_client.loop_start()

    def disconnect(self) -> None:
        self.__mqtt_client.disconnect()

    def subscribe(self, session: Session, on_downlink: Callable[[Frame], None]) -> None:
        def on_connect(client, userdata, flags, rc):
            self.__logger.info('GRID MQTT Client subscribing')
            client.subscribe(topic=build_downlink_topic(session))

        self.__mqtt_client.on_connect = on_connect

        def on_message(client, userdata, msg: MQTTMessage):
            frame_dict = json.loads(msg.payload)
            frame = frame_from_dict(frame_dict)
            frame.session = session  # Set session explicitly as frame_dict['communicationSession']  does not have GroundStation and Satellite
            on_downlink(frame)

        self.__mqtt_client.on_message = on_message

    def send(self, session: Session, raw_data: bytes) -> MQTTMessageInfo:
        self.__logger.info('Grid MQTT Client send')
        # @TODO implement check for on connect
        return self.__mqtt_client.publish(topic=build_uplink_topic(session), payload=raw_data)
