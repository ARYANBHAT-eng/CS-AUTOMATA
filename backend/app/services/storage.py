from typing import Dict, Optional

from app.models.activity import Activity
from app.models.user import User


users_db: Dict[str, User] = {}
activity_db: Dict[str, Activity] = {}


def create_user(user: User) -> User:
    if user.user_id in users_db:
        raise ValueError("User already exists")

    users_db[user.user_id] = user
    return user


def get_user(user_id: str) -> Optional[User]:
    return users_db.get(user_id)


def update_activity(activity: Activity) -> Activity:
    existing_activity = activity_db.get(activity.user_id)

    if existing_activity is None:
        activity_db[activity.user_id] = activity
        return activity

    updated_activity = Activity(
        user_id=activity.user_id,
        last_active_date=activity.last_active_date,
        login_count=existing_activity.login_count + activity.login_count,
        feature_usage_score=activity.feature_usage_score,
    )
    activity_db[activity.user_id] = updated_activity
    return updated_activity


def get_activity(user_id: str) -> Optional[Activity]:
    return activity_db.get(user_id)
