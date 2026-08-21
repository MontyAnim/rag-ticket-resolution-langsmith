from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
import uuid
from src.models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    tenant_id = Column(String, index=True, nullable=False, doc="Tenant ID for data isolation")
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    thread_id = Column(String, nullable=True, doc="LangGraph thread ID")
    query = Column(Text, nullable=False)

    user = relationship("User")
