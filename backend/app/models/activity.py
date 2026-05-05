from datetime import datetime

from pydantic import BaseModel, Field


class Activity(BaseModel):
    user_id: str
    last_active_date: datetime
    login_count: int = Field(..., ge=0)
    feature_usage_score: float = Field(..., ge=0)
