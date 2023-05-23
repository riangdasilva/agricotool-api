from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints.auth import router as auth_router
from .api.endpoints.measures import router as measures_router
from .api.endpoints.feedbacks import router as feedbacks_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(measures_router)
app.include_router(feedbacks_router)
