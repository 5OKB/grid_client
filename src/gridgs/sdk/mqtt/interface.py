from abc import ABC, abstractmethod
from typing import Callable

from paho.mqtt.client import MQTTMessageInfo

from gridgs.sdk.entity.frame import Frame
from gridgs.sdk.entity.session import Session


class Connector(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass


class Subscriber(ABC):
    @abstractmethod
    def subscribe(self, session: Session, on_downlink: Callable[[Frame], None]) -> None:
        pass


class Sender(ABC):
    @abstractmethod
    def send(self, session: Session, raw_data: bytes) -> MQTTMessageInfo:
        pass
