from pydantic import BaseModel


class UrlValidator(BaseModel):
    input_url: str
