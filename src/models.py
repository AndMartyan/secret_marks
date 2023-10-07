import uuid
from sqlalchemy import Column, LargeBinary, Integer, String, DateTime, func
from database import Base


class Secret(Base):
    __tablename__ = 'secrets'

    id = Column(String, primary_key=True, index=True)
    secret_text = Column(LargeBinary, index=True)
    passphrase = Column(LargeBinary)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    lifetime_minutes = Column(Integer)

