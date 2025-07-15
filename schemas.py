from pydantic import BaseModel
from datetime import date

class MessageSearch(BaseModel):
    message_id: int
    channel_name: str
    post_text: str
    post_date: date

    class Config:
        orm_mode = True

class TopProduct(BaseModel):
    object_label: str
    count: int

class ChannelActivity(BaseModel):
    channel_id: int
    post_count: int
    first_post: str
    last_post: str

    class Config:
        from_attributes = True  # For Pydantic V2




