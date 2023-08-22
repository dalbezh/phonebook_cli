from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class PhonebookData(BaseModel):
    id: int
    last_name: str
    middle_name: str = ""
    first_name: str
    organization: str = ""
    work_phone: PhoneNumber = ""
    personal_phone: PhoneNumber
