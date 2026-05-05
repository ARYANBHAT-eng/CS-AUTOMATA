from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    email: str
    signup_date: datetime
    plan_type: Literal["free", "pro", "enterprise"]
