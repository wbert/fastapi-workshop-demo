from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    price_cents: int = Field(ge=0)


class ItemRead(BaseModel):
    id: int
    name: str
    description: str
    price_cents: int

    class Config:
        from_attributes = True
