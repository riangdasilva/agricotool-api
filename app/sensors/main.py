from fastapi import APIRouter

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


@router.post("/")
async def create_sensor():
    return {}


@router.get("/")
async def read_sensors():
    return {}


@router.get("/{sensor_id}")
async def read_sensor():
    return {}


@router.put("/{sensor_id}")
async def update_sensor():
    return {}


@router.delete("/{sensor_id}")
async def delete_sensor():
    return {}
