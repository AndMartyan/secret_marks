import uuid
from fastapi import FastAPI, HTTPException
from database import Base, engine, SessionLocal
from models import Secret
from schemas import SecretRequest, SecretResponse
from encryption import fernet
from datetime import datetime, timedelta

# Инициализация приложения
app = FastAPI(title="Secret marks")

# Создание таблицы в базе данных, если её нет
Base.metadata.create_all(bind=engine)


@app.post("/generate", response_model=SecretResponse)
async def generate_secret(request: SecretRequest):
    # Шифрование секрета
    encrypted_secret = fernet.encrypt(request.secret.encode())
    # Шифрование кодовой фразы
    encrypted_passphrase = fernet.encrypt(request.passphrase.encode())
    # Вычисление времени жизни секрета
    lifetime = datetime.now() + timedelta(minutes=request.lifetime_minutes)
    # Сохранение данных в базе
    db_secret = Secret(id=str(uuid.uuid4()), secret_text=encrypted_secret, passphrase=encrypted_passphrase,
                       lifetime_minutes=request.lifetime_minutes)
    db = SessionLocal()
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return {"secret_key": str(db_secret.id), "lifetime": lifetime}


@app.get("/secrets/{secret_key}", response_model=SecretResponse)
async def get_secret(secret_key: str, passphrase: str):
    db = SessionLocal()
    # Поиск секрета в базе данных
    secret = db.query(Secret).filter(Secret.id == secret_key).first()
    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    # Расшифровка секретной фразы
    decrypted_passphrase = fernet.decrypt(secret.passphrase).decode()
    # Проверка соответствия фраз
    if decrypted_passphrase == passphrase:
        now = datetime.now()
        # Проверка expire-периода
        if now <= secret.created_at + timedelta(minutes=secret.lifetime_minutes):
            # Расшифровка секрета
            decrypted_secret = fernet.decrypt(secret.secret_text).decode()
            # Удаление секрета
            db.delete(secret)
            db.commit()
            return {"secret_key": decrypted_secret,
                    "lifetime": secret.created_at + timedelta(minutes=secret.lifetime_minutes)}
        else:
            # Удаление секрета по expire-периоду
            db.delete(secret)
            db.commit()
            raise HTTPException(status_code=400, detail="Secret has expired")
    else:
        raise HTTPException(status_code=404, detail="Secret not found")
