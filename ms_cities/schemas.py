from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
