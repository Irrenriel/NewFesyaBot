from pydantic import BaseModel


class ChatInfo(BaseModel):
    id: int

    new_loc_ntf: bool
    delete_loc_ntf: bool

    brief_log: bool
    brief_mode: bool

    craft_ntf: bool
