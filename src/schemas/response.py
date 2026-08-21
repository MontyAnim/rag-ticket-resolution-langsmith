from pydantic import BaseModel, Field
from typing import Optional, Any

class SystemResponse(BaseModel):
    status: str = Field(..., description="Estado de la respuesta, e.g., 'success', 'error'.")
    message: str = Field(..., description="Mensaje detallando el resultado de la operación.")
    data: Optional[Any] = Field(default=None, description="Carga útil opcional de la respuesta.")

class TicketResolutionResponse(BaseModel):
    answer: str = Field(
        ..., 
        description="La respuesta estructurada generada por el agente para resolver el ticket."
    )
    trace_id: str = Field(
        ..., 
        description="Identificador de ejecución raíz (Root Run) de LangSmith, obligatorio para el feedback asíncrono."
    )
    thread_id: Optional[str] = Field(
        default=None, 
        description="Identificador del hilo de conversación devuelto para mantener la continuidad en el cliente."
    )
