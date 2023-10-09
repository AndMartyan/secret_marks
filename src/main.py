import uuid

from fastapi import FastAPI, HTTPException, Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete

from models import secret
from schemas import SecretRequest, SecretResponse, FinalResponse
from encryption import hash_text, match_hashed_text, secret_encode, secret_decode

# Инициализация приложения
app = FastAPI(title="Secret marks")


@app.post("/generate", response_model=SecretResponse)
async def generate_secret(request: SecretRequest,
                          session: AsyncSession = Depends(get_async_session)):
    """Метод  принимает секрет и кодовую фразу и отдает `secret_key` по которому этот секрет можно получить."""
    hashed_secret = hash_text(request.secret, request.passphrase)
    encrypted_secret = secret_encode(request.secret, hashed_secret)
    # Сохранение данных в базе
    secret_key = str(uuid.uuid4().hex)
    stmt = insert(secret).values(id=secret_key, secret_text=encrypted_secret, hash=hashed_secret)
    await session.execute(stmt)
    await session.commit()
    return {"secret_key": secret_key}


@app.get("/secrets/{secret_key}", response_model=FinalResponse)
async def get_secret(passphrase: str,
                     secret_key: str,
                     session: AsyncSession = Depends(get_async_session)):
    """Метод принимает на вход кодовую фразу и отдает секрет."""
    # Поиск секрета в базе данных
    stmt = select(secret).filter(secret.c.id == secret_key)
    result = await session.execute(stmt)
    db_entry = result.all()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Secret not found")
    decrypted_secret = secret_decode(encoded=db_entry[0][1], key=db_entry[0][2])
    # Проверка соответствия фраз
    if match_hashed_text(hashed_text=db_entry[0][2], secret=decrypted_secret, user_salt=passphrase):
        query = delete(secret).where(secret.c.id == secret_key)
        await session.execute(query)
        await session.commit()
        return {"secret": decrypted_secret}
    else:
        raise HTTPException(status_code=404, detail="Secret not found")
