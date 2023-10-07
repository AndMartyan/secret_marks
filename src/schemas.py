from pydantic import BaseModel
from datetime import datetime


class SecretRequest(BaseModel):
    secret: str
    passphrase: str
    lifetime_minutes: int


class SecretResponse(BaseModel):
    secret_key: str
    lifetime: datetime
