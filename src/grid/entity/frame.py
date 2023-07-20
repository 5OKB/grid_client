import uuid

from application.grid.entity.session import Session


class Frame:
    __id: uuid.UUID
    __session: Session
    __raw_data: bytes

    def __init__(self, id: uuid.UUID, session: Session, raw_data: bytes):
        self.__id = id
        self.__session = session
        self.__raw_data = raw_data

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def raw_data(self) -> bytes:
        return self.__raw_data
