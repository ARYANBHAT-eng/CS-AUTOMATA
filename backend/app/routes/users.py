from fastapi import APIRouter, HTTPException

from app.models.response import APIResponse
from app.models.user import User
from app.services.scoring import compute_user_score
from app.services.storage import create_user, get_activity, get_user
from app.services.workflow import generate_workflow_actions


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=APIResponse)
def create_user_endpoint(user: User):
    try:
        saved_user = create_user(user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "message": "User created successfully",
        "data": {"user": saved_user.model_dump()},
    }


@router.get("/{user_id}", response_model=APIResponse)
def get_user_metrics(user_id: str):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    activity = get_activity(user_id)

    return {
        "status": "success",
        "message": "User metrics fetched successfully",
        "data": {
            "user": user.model_dump(),
            "activity": activity.model_dump() if activity else None,
        },
    }


@router.get("/{user_id}/score", response_model=APIResponse)
def get_user_score(user_id: str):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    activity = get_activity(user_id)
    score = compute_user_score(user, activity)

    return {
        "status": "success",
        "message": "User score computed successfully",
        "data": score,
    }


@router.get("/{user_id}/workflow", response_model=APIResponse)
def get_user_workflow(user_id: str):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    activity = get_activity(user_id)
    score = compute_user_score(user, activity)
    actions = generate_workflow_actions(score)

    return {
        "status": "success",
        "message": "Workflow actions generated successfully",
        "data": {
            "user_id": user.user_id,
            "score": score,
            "actions": actions,
        },
    }
