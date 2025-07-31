import os, jwt, bcrypt, re
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator
from app.config import settings
import pymongo
from pymongo import AsyncMongoClient



client = AsyncMongoClient(os.environ["MONGODB_URL"], 
                          server_api =pymongo.server_api.ServerApi(version="1",strict=True, deprecation_errors=True), 
                          uuidRepresentation="standard")

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+"     
    r"@"                      
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"   
)
# Connect to the DB and create the collection "users"
db = client.get_default_database()
users_collection = db.get_collection("users")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await users_collection.create_index("email", unique=True)
    yield

app = FastAPI(title="Prueba Técnica", lifespan=lifespan)

# Classes
class Phone(BaseModel):
    number: str
    citycode: str
    countrycode: str = Field(..., alias="contrycode")

class InputModel(BaseModel):
    name: str
    email: str
    password: str
    phones: list[Phone]
    # Validate the reequirements of the password
    @field_validator("password")
    @classmethod
    def password_rules(cls, v: str) -> str:
        if len(v) < 8:
            raise HTTPException(422, detail={"mensaje": "La contraseña debe tener al menos 8 carácteres"})
        if not re.search(r"[A-Z]", v):
            raise HTTPException(422, detail={"mensaje": "Debe incluir una mayuscula"})
        if not re.search(r"[a-z]", v):
            raise HTTPException(422, detail={"mensaje": "Debe incluir una minúscula"})
        if len(re.findall(r"\d", v)) < 2:
            raise HTTPException(422, detail={"mensaje": "Debe haber al menos 2 dígitos"})
        return v
    
    @field_validator("email")
    @classmethod
    def email_rules(cls, v: str) -> str:
        if " " in v:
            raise HTTPException(422, detail={"mensaje": "El correo no debe tener espacios"})
        if not EMAIL_RE.fullmatch(v):
            raise HTTPException(422, detail={"mensaje": "Formato erroneo, debe correo de ejemplo: aaaa@dominio.cl"})
        return v

class OutputModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    phones: list[Phone]
    id: str
    created: datetime
    modified: datetime
    last_login: datetime
    token: str
    isactive: bool = True

class UserModelDB(BaseModel):
    id: str
    name: str
    email: EmailStr
    password_hash: str
    phones: list[Phone]
    created: datetime
    modified: datetime
    last_login: datetime
    token: str
    isactive: bool = True

@app.post("/register", response_model=OutputModel, status_code=201)
async def register(input: InputModel):
    
    #Check if there is a registered user
    if await users_collection.find_one({"email": input.email}):
        raise HTTPException(409, detail={"mensaje": "Usuario ya registrado"})
    
    #If not registered get the time and create the JWT token
    now = datetime.now(timezone.utc)
    aux_uuid = uuid4()
    payload = {
        "uuid": str(aux_uuid),
        "email": input.email,
        "emited": now.timestamp(),
        "expire": int((now + timedelta(minutes=15)).timestamp()) 
    }
    jwt_token = jwt.encode(payload=payload, key=settings.jwt_private_key, algorithm="HS256")
    # Create the object user in the way to organize the data and fast save/return 
    new_user = UserModelDB(
        id = str(aux_uuid),
        name = input.name,
        email = input.email,
        password_hash= bcrypt.hashpw(input.password.encode("utf-8"),bcrypt.gensalt()),   # Hashed Password stored in DB, but not when it's returned
        phones = input.phones,
        created = now,
        modified = now,
        last_login = now,
        token = jwt_token,
        isactive = True
    )
    # Register the user into the DB in JSON format
    await users_collection.insert_one(new_user.model_dump(by_alias=True))
    output = OutputModel(
        id = str(aux_uuid),
        name = input.name,
        email = input.email,
        password= input.password,   # Hashed Password stored in DB, but the password returned is not hashed
        phones = input.phones,
        created = now,
        modified = now,
        last_login = now,
        token = jwt_token,
        isactive = True
    )
    return output
    