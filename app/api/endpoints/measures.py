from fastapi import APIRouter, HTTPException, Depends
from ...api.endpoints.auth import get_current_user, authenticate_api_key
from ...core.database import database
from ..models.measures import MeasureCreate, Measure
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/measures",
    tags=["measures"]
)


def filter_between_dates(measures, start_date, end_date):
    return [measure for measure in measures if start_date <= measure["timestamp"] <= end_date]


def measure_serializer(measure):
    return {
        "id": str(measure["_id"]),
        "owner_id": str(measure["owner_id"]),
        "temperature": measure["temperature"],
        "humidity": measure["humidity"],
        "timestamp": measure["timestamp"],
    }


def measures_serializer(measures):
    return [measure_serializer(measure) for measure in measures]


@router.post("/", response_model=Measure)
async def create_measure(measure: MeasureCreate):

    user = authenticate_api_key(measure.api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    measure = dict(measure)

    new_measure = {
        "owner_id": ObjectId(user["id"]),
        "temperature": measure["temperature"],
        "humidity": measure["humidity"],
        "timestamp": measure["timestamp"],
    }

    created_measure = database.measures.insert_one(new_measure).inserted_id

    return measure_serializer(database.measures.find_one({"_id": created_measure}))


@router.get("/", response_model=list[Measure])
async def read_measures(user=Depends(get_current_user), start_date: str = None, end_date: str = None):
    measures = list(database.measures.find({"owner_id": ObjectId(user["id"])}))
    if start_date and end_date:
        measures = filter_between_dates(
            measures, start_date, end_date)
    return measures_serializer(measures)


@router.get("/{measure_id}", response_model=Measure)
async def read_measure(measure_id: str, user=Depends(get_current_user)):
    measure = database.measures.find_one(
        {"_id": ObjectId(measure_id), "owner_id": ObjectId(user["id"])})
    if not measure:
        raise HTTPException(status_code=404, detail="Measure not found")
    return measure_serializer(measure)


@router.put("/{measure_id}", response_model=Measure)
async def update_measure(measure_id: str, measure: MeasureCreate, user=Depends(get_current_user)):
    measure = dict(measure)
    measure["owner_id"] = ObjectId(user["id"])
    database.measures.update_one({"_id": ObjectId(measure_id)}, {
                                 "$set": measure}, upsert=False)
    return measure_serializer(measure)


@router.delete("/{measure_id}", response_model=Measure)
async def delete_measure(measure_id: str, user=Depends(get_current_user)):
    measure = database.measures.find_one(
        {"_id": ObjectId(measure_id), "owner_id": ObjectId(user["id"])})
    if not measure:
        raise HTTPException(status_code=404, detail="Measure not found")
    database.measures.delete_one({"_id": ObjectId(measure_id)})
    return measure_serializer(measure)
