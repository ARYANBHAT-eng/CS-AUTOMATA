from fastapi import APIRouter, HTTPException

from app.models.activity import Activity
from app.models.response import APIResponse
from app.services.storage import get_user, update_activity


router = APIRouter(prefix="/activity", tags=["activity"])


@router.post("/update", response_model=APIResponse)
def update_activity_endpoint(activity: Activity):
    if get_user(activity.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    saved_activity = update_activity(activity)
    return {
        "status": "success",
        "message": "Activity updated successfully",
        "data": {"activity": saved_activity.model_dump()},
    }
