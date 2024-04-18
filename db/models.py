from pydantic import BaseModel


class UrlModel(BaseModel):
    input_url: str
    hashed_url: str
