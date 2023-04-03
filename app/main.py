from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings

from .measures import main as measures_main
from .sensors import main as sensors_main
from .users import main as users_main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# def startup_db_client():
#    app.mongodb_client = MongoClient(settings.DB_URL)
#    app.database = app.mongodb_client[settings.DB_NAME]
#
#
# @app.on_event("shutdown")
# def shutdown_db_client():
#    app.mongodb_client.close()


app.include_router(measures_main.router)
app.include_router(sensors_main.router)
app.include_router(users_main.router)
