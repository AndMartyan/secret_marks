from pydantic import BaseModel


class SecretRequest(BaseModel):
    secret: str
    passphrase: str


class SecretResponse(BaseModel):
    secret_key: str


class FinalResponse(BaseModel):
    secret: str

