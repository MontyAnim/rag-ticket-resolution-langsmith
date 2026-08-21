from pydantic import BaseModel, Field
from typing import Optional

class TicketCreate(BaseModel):
    tenant_id: str = Field(
        ..., 
        description="Identificador único del cliente corporativo u organización (para aislamiento de datos y agregación de costos)."
    )
    user_id: str = Field(
        ..., 
        description="Identificador del usuario final (para rastrear la satisfacción y sesiones)."
    )
    thread_id: Optional[str] = Field(
        default=None, 
        description="Identificador del hilo de conversación para LangGraph (para reanudar conversaciones multi-turno)."
    )
    query: str = Field(
        ..., 
        description="El texto o consulta del ticket en sí."
    )
