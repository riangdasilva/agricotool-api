from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ...core.database import database
from ...core.settings import settings

from bson.objectid import ObjectId


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = {"username": username}
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = readUserByUsername(username=token_data["username"])
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return {
        "username": user["username"],
        "id": str(user["_id"]),
        "hashed_password": user["hashed_password"],
    }


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_api_key():
    return pwd_context.hash(datetime.now().isoformat() + SECRET_KEY)


def authenticate_api_key(api_key: str):
    user = database.users.find_one({"api_key": api_key})
    if not user:
        return False
    return {"username": user["username"], "id": str(user["_id"])}


def authenticate_user(username: str, password: str):
    user = readUserByUsername(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def readUserByUsername(username: str):
    user = database.users.find_one({"username": username})
    if user:
        return user
    return None


def createUser(username: str, password: str):
    user = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "api_key": "",
    }
    created_user = database.users.insert_one(user)
    new_user = database.users.find_one({"_id": created_user.inserted_id})
    return {
        "username": new_user["username"],
        "id": str(new_user["_id"]),
    }


@router.post("/change-password")
async def change_password(
    old_password: str, new_password: str, user: dict = Depends(get_current_user)
):
    if not verify_password(old_password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    new_password_hash = get_password_hash(new_password)

    database.users.update_one(
        {"_id": ObjectId(user["id"])}, {"$set": {"hashed_password": new_password_hash}}
    )

    return {"message": "Password changed"}


@router.post("/signup")
async def signup(username: str, password: str):
    if readUserByUsername(username):
        return {"message": "Username already exists"}

    return createUser(username, password)


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/@me")
async def read_current_user(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "id": user["id"],
    }


@router.post("/api_key")
async def generate_api_key(user: dict = Depends(get_current_user)):
    new_api_key = pwd_context.hash(create_api_key())

    database.users.update_one(
        {"_id": ObjectId(user["id"])}, {"$set": {"api_key": new_api_key}}
    )

    return {"api_key": new_api_key}


@router.post("/recover-password")
async def recover_password(username: str):
    user = readUserByUsername(username)
