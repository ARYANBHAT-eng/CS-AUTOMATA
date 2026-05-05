from datetime import datetime, timezone
from typing import Dict, Optional

from app.models.activity import Activity
from app.models.user import User


def compute_user_score(user: User, activity: Optional[Activity]) -> Dict:
    if activity is None:
        return {
            "user_id": user.user_id,
            "engagement_score": 0,
            "inactivity_days": None,
            "churn_risk": "high",
            "user_segment": "at_risk",
        }

    now_utc = datetime.now(timezone.utc)
    last_active_date = activity.last_active_date

    if last_active_date.tzinfo is None or last_active_date.utcoffset() is None:
        last_active_utc = last_active_date.replace(tzinfo=timezone.utc)
    else:
        last_active_utc = last_active_date.astimezone(timezone.utc)

    inactivity_days = (now_utc - last_active_utc).days
    normalized_logins = min(activity.login_count / 10, 1) * 100
    engagement_score = min(
        (normalized_logins * 0.4) + (activity.feature_usage_score * 0.6),
        100,
    )
    engagement_score = round(engagement_score, 2)

    if inactivity_days > 14:
        churn_risk = "high"
    elif inactivity_days >= 7:
        churn_risk = "medium"
    else:
        churn_risk = "low"

    if churn_risk == "high":
        user_segment = "at_risk"
    elif engagement_score > 70:
        user_segment = "power_user"
    else:
        user_segment = "active"

    return {
        "user_id": user.user_id,
        "engagement_score": engagement_score,
        "inactivity_days": inactivity_days,
        "churn_risk": churn_risk,
        "user_segment": user_segment,
    }
