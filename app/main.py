from fastapi import FastAPI, Depends, HTTPException
from app.core.schema import PasswordConfig, PasswordGenerated, StrongnessGenerated
from app.core.logic import generate_password, password_strongness
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None,
              redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/passgen/generate")
async def passgen_generate(password_config: PasswordConfig = Depends()) -> PasswordGenerated:

    if not any(value == True for value in password_config.dict().values()):
        raise HTTPException(
            status_code=400, detail=f"You can't create a password that has no chars")

    if password_config.length < 4:
        raise HTTPException(
            status_code=400, detail=f"You can't create a password smaller than 4 chars")

    (password, strongness) = generate_password(**password_config.dict())

    return PasswordGenerated(password=password, strongness=strongness)


@app.get("/passgen/check")
async def passgen_check(password: str) -> StrongnessGenerated:

    if len(password) < 4:
        raise HTTPException(
            status_code=400, detail=f"You can't create a password smaller than 4 chars")

    return StrongnessGenerated(strongness=password_strongness(password))


@app.get("/{path:path}")
async def catch_all(path: str):
    raise HTTPException(
        status_code=404, detail=f"Path not found: /{path}, to generate a password use /passgen/generate endpoint and to check a password use /passgen/check/'your-password'")
