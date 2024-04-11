from pydantic import BaseModel, HttpUrl


class UrlValidator(BaseModel):
    input_url: HttpUrl