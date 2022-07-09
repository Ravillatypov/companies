from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """Base response model schema."""

    class Config:  # noqa: WPS431, WPS306, D106, D204
        orm_mode = True
