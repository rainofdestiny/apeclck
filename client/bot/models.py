from pydantic import BaseModel


class CreateRequest(BaseModel):
    url: str
    name: str
    enable_logger: bool
    ttl: int  # seconds
