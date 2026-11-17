from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class ItemCreate(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    stock: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)
    unit: str = Field(default="UN", min_length=1)
    location: str = Field(default="PRATELEIRA", min_length=1)

    @field_validator("sku", "name", "unit", "location")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode estar vazio")
        return value


class ItemPatch(BaseModel):
    sku: str | None = Field(default=None, min_length=1)
    name: str | None = Field(default=None, min_length=1)
    min_stock: int | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None, min_length=1)


class ItemOut(ItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovementCreate(BaseModel):
    type: Literal["IN", "OUT", "ADJUST"]
    quantity: int = Field(ge=0)
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_quantity(self):
        if self.type in ("IN", "OUT") and self.quantity == 0:
            raise ValueError(
                "Movimentações IN e OUT exigem quantidade maior que zero"
            )

        return self


class MovementOut(BaseModel):
    id: int
    item_id: int
    type: str
    quantity: int
    reason: str
    stock_before: int
    stock_after: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class AlertOut(BaseModel):
    id: int
    item_id: int
    status: Literal["OPEN", "RESOLVED"]
    created_at: str
    resolved_at: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ScanResult(BaseModel):
    opened: int
    resolved: int


class HelpRequest(BaseModel):
    question: str = Field(min_length=1)
    max_sources: int = Field(default=3, ge=1, le=10)


class HelpSource(BaseModel):
    id: str
    title: str


class HelpResponse(BaseModel):
    answer: str
    sources: list[HelpSource]
    provider: str
    model: str
