from sqlalchemy import Column, String
from src.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, doc="ID match with frontend/auth provider")
    tenant_id = Column(String, index=True, nullable=False, doc="Organization or Tenant ID")
