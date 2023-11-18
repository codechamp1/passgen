from pydantic import BaseModel

# Pydantic schemas for validating requests and responses.


class PasswordConfig(BaseModel):
    length: int = 14
    uppercase: bool = True
    lowercase: bool = True
    digits: bool = True
    special_char: bool = True


class PasswordGenerated(BaseModel):
    password: str
    strongness: str


class StrongnessGenerated(BaseModel):
    strongness: str
