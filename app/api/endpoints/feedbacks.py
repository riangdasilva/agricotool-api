from fastapi import APIRouter, HTTPException, Depends
from ...api.endpoints.auth import get_current_user
from ...core.database import database
from bson.objectid import ObjectId

from ...api.models.feedbacks import Feedback, FeedbackCreate

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])


def feedback_serializer(feedback):
    return {
        "id": str(feedback["_id"]),
        "owner_id": str(feedback["owner_id"]),
        "message": feedback["message"],
        "timestamp": feedback["timestamp"],
    }


def feedbacks_serializer(feedbacks):
    return [feedback_serializer(feedback) for feedback in feedbacks]


@router.post("/", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate, user=Depends(get_current_user)):
    feedback = dict(feedback)

    new_feedback = {
        "owner_id": ObjectId(user["id"]),
        "message": feedback["message"],
        "timestamp": feedback["timestamp"],
    }

    created_feedback = database.feedbacks.insert_one(new_feedback).inserted_id

    return feedback_serializer(database.feedbacks.find_one({"_id": created_feedback}))


@router.get("/", response_model=list[Feedback])
async def read_feedbacks(user=Depends(get_current_user)):
    return feedbacks_serializer(
        list(database.feedbacks.find({"owner_id": ObjectId(user["id"])}))
    )


@router.delete("/{feedback_id}", response_model=Feedback)
async def delete_feedback(feedback_id: str, user=Depends(get_current_user)):
    feedback = database.feedbacks.find_one(
        {"_id": ObjectId(feedback_id), "owner_id": ObjectId(user["id"])}
    )
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    database.feedbacks.delete_one({"_id": ObjectId(feedback_id)})
    return feedback_serializer(feedback)
