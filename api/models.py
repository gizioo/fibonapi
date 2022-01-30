from pydantic import BaseModel


class ResponseModel(BaseModel):
    result: int
