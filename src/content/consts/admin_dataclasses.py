from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class ActiveLog:
    # Main info
    id: int
    username: str

    # User message
    data: str

    # Datetime
    time: time
    date: datetime
