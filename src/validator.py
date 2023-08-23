from typing import Union

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class CreateField(BaseModel):
    """Используется при создании записи"""
    id: int
    last_name: str
    first_name: str
    middle_name: str = ""
    organization: str = ""
    work_phone: str = ""
    personal_phone: PhoneNumber


class PhoneField(BaseModel):
    """Для приведения поискового запроса в табличному типу"""
    phone: Union[PhoneNumber, str]
