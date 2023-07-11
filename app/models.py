from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from .database import Base

# user table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    activation_code = Column(String(255), nullable=False)
    activation_status = Column(String(10), default=text('false'), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class CachedData(Base):
    __tablename__ = "cached_data"
    id = Column(Integer, primary_key=True, nullable=False)
    cache_key = Column(String(255), unique=True)
    data = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))