from pydantic import BaseModel, Field, ConfigDict


class MessageRequest(BaseModel):
    message: str
    to: str
    sender: str = Field(alias="from")
    timeToLifeSec: int

    model_config = ConfigDict(populate_by_name=True)


class MessageResponse(BaseModel):
    message: str
