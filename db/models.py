from pydantic import BaseModel


class UrlModel(BaseModel):
    url: str
    hashed_url: str
