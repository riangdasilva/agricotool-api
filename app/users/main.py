from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@ router.post("/")
async def create_user():
    return {}


@ router.get("/")
async def read_users():
    return {}


@ router.get("/{user_id}")
async def read_user():
    return {}


@ router.put("/{user_id}")
async def update_user():
    return {}


@ router.delete("/{user_id}")
async def delete_user():
    return {}
