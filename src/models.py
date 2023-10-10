from sqlalchemy import Column, LargeBinary, String, Table
from sqlalchemy import MetaData

metadata = MetaData()
secret = Table(
    "secrets",
    metadata,
    Column("id", String, primary_key=True, index=True),
    Column("secret_text", LargeBinary, nullable=False),
    Column("hash", String, nullable=False)
)
