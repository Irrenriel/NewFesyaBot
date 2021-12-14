from dataclasses import dataclass


@dataclass
class ActiveLog:
    # Main info
    id: int
    username: str

    # User message
    info: str

    # Datetime
    time: int
    date: str
