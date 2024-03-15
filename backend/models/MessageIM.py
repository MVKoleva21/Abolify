from pydantic import BaseModel

class MessageIM(BaseModel):
    content: str
    chat_id: int