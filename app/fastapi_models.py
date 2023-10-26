from pydantic import BaseModel


class Answer(BaseModel):
    latitude: str
    longitude: str