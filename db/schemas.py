from pydantic import BaseModel


class UrlValidator(BaseModel):
    url: str
