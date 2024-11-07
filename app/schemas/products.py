from pydantic import BaseModel, Field, ConfigDict


class SProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(
        ...,
        min_length=1, max_length=30,
        description="Название товара")

    description: str = Field(
        None,
        min_length=1, max_length=50,
        description="Описание товара")

    price: int = Field(
        ...,
        description="Цена товара")

    count: int = Field(
        0,
        description="Количество товара")


class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        min_length=1, max_length=30,
        description="Название товара")

    description: str = Field(
        None,
        min_length=1, max_length=50,
        description="Описание товара")

    price: int = Field(
        ...,
        description="Цена товара")

    count: int = Field(
        0,
        description="Количество товара")

class SProductUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    description: str | None = Field(None, min_length=1, max_length=50)
    price: int | None = None
    count: int | None = None