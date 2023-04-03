from fastapi import APIRouter

router = APIRouter(
    prefix="/measures",
    tags=["measures"],
)


@router.post("/")
async def create_measure():
    return {}


@router.get("/")
async def read_measures():
    return {}


@router.get("/{measure_id}")
async def read_measure():
    return {}


@router.put("/{measure_id}")
async def update_measure():
    return {}


@router.delete("/{measure_id}")
async def delete_measure():
    return {}
