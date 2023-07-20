import uuid
from datetime import datetime

from application.grid.entity.ground_station import GroundStation
from application.grid.entity.horizontal_coords import HorizontalCoords, horizontal_coords_to_dict, \
    horizontal_coords_from_dict
from application.grid.entity.satellite import Satellite


class Session:
    _id: uuid.UUID
    _satellite: Satellite
    _ground_station: GroundStation
    _start_datetime: datetime
    _end_datetime: datetime
    _status: str
    _tca_coords: HorizontalCoords

    STATUS_SCHEDULED = 'scheduled'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    def __init__(self, id: uuid.UUID, satellite: Satellite, ground_station: GroundStation,
                 start_datetime: datetime, end_datetime: datetime,
                 status: str, tca_coords: HorizontalCoords):
        self._id = id
        self._satellite = satellite
        self._ground_station = ground_station
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._status = status
        self._tca_coords = tca_coords

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def satellite(self) -> Satellite:
        return self._satellite

    @property
    def ground_station(self) -> GroundStation:
        return self._ground_station

    @property
    def start_datetime(self) -> datetime:
        return self._start_datetime

    @property
    def end_datetime(self) -> datetime:
        return self._end_datetime

    @property
    def status(self) -> str:
        return self._status

    def statuses(self) -> list:
        return [self.STATUS_SCHEDULED, self.STATUS_IN_PROGRESS, self.STATUS_SUCCESS, self.STATUS_FAILED]

    @property
    def tca_coords(self) -> HorizontalCoords:
        return self._tca_coords

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'status': self.status,
            'satellite': {'id': self.satellite.id},
            'groundStation': {'id': self.ground_station.id},
            'startDateTime': self.start_datetime.isoformat(sep='T', timespec='auto'),
            'endDateTime': self.end_datetime.isoformat(sep='T', timespec='auto'),
            'tcaCoords': horizontal_coords_to_dict(self.tca_coords)
        }


def session_from_dict(ses: dict) -> Session:
    return Session(
        id=uuid.UUID(ses['id']),
        satellite=Satellite(ses['satellite']['id']),
        ground_station=GroundStation(ses['groundStation']['id']),
        status=ses['status'],
        start_datetime=datetime.fromisoformat(ses['startDateTime']),
        end_datetime=datetime.fromisoformat(ses['endDateTime']),
        tca_coords=horizontal_coords_from_dict(ses['tcaCoords'])
    )
