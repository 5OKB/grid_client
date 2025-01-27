import base64
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from .session import Session, session_from_dict


@dataclass(frozen=True)
class Frame:
    id: uuid.UUID
    created_at: datetime
    session: Session
    raw_data: bytes
    extra_data: dict = None


def frame_from_dict(fr: dict) -> Frame:
    # @TODO if no session build from groundstation and sputnik
    session = session_from_dict(fr['communicationSession'])
    return Frame(
        id=uuid.UUID(fr['id']),
        created_at=datetime.fromisoformat(fr['createdAt']) if 'createdAt' in fr else None,
        session=session,
        raw_data=base64.b64decode(fr['rawData']) if 'rawData' in fr else None,
        extra_data=fr['extraData'] if 'extraData' in fr else None)
