from typing import Union, Optional

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class CreateField(BaseModel):
    """Используется при создании записи"""
    id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = ""
    organization: Optional[str] = ""
    work_phone: Optional[str] = ""
    personal_phone: PhoneNumber


class PhoneField(BaseModel):
    """Для приведения поискового запроса в табличному типу"""
    phone: Union[PhoneNumber, str]
