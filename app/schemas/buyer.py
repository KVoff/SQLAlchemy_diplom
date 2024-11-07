from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class SAddress(BaseModel):
    id: int
    city: str
    street: str
    house_number: str


class SBuyer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    phone_number: str = Field(
        ...,
        description="Номер телефона в международном формате, начинающийся с '+'")

    first_name: str = Field(
        ...,
        min_length=1, max_length=50,
        description="Имя покупателя, от 1 до 50 символов")

    last_name: str = Field(
        ...,
        min_length=1, max_length=50,
        description="Фамилия покупателя, от 1 до 50 символов")

    date_of_birth: date = Field(
        ...,
        description="Дата рождения покупателя в формате ГГГГ-ММ-ДД")

    email: EmailStr = Field(
        ...,
        description="Электронная почта покупателя")

    special_notes: Optional[str] = Field(
        None, max_length=500,
        description="Дополнительные заметки, не более 500 символов")

    address: Optional[List[SAddress]] = Field(None, description="Адрес")

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

    @field_validator("date_of_birth", mode="before")
    def validate_date_of_birth(cls, value):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value


class SBuyerAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    phone_number: str = Field(
        ...,
        description="Номер телефона в международном формате, начинающийся с '+'")

    first_name: str = Field(
        ...,
        min_length=1, max_length=50,
        description="Имя покупателя, от 1 до 50 символов")

    last_name: str = Field(
        None,
        min_length=1, max_length=50,
        description="Фамилия покупателя, от 1 до 50 символов")

    date_of_birth: date = Field(
        ...,
        description="Дата рождения покупателя в формате ГГГГ-ММ-ДД")

    email: EmailStr = Field(
        None,
        description="Электронная почта покупателя")

    special_notes: Optional[str] = Field(
        None, max_length=500,
        description="Дополнительные заметки, не более 500 символов")


    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value

    @field_validator("date_of_birth", mode="before")
    def validate_date_of_birth(cls, value):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value