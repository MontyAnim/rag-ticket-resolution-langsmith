from src.models.base import Base
from src.models.user import User
from src.models.ticket import Ticket

# Explicitly export Base for Alembic target_metadata
__all__ = ["Base", "User", "Ticket"]
