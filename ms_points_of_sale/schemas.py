from pydantic import BaseModel, ConfigDict


class PointOfSaleBase(BaseModel):
    name: str
    address: str
    city: str


class PointOfSaleCreate(PointOfSaleBase):
    pass


class PointOfSaleUpdate(PointOfSaleBase):
    pass


class PointOfSaleResponse(PointOfSaleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
