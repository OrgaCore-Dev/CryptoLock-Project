"""
Módulo de modelos e schemas de dados.
Define as estruturas de dados utilizadas na aplicação.
"""

from typing import Optional
from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    """Modelo para mensagens recebidas do webhook do WhatsApp."""
    
    entry: list[dict] = Field(..., description="Lista de entradas do webhook")


class TextMessage(BaseModel):
    """Modelo para mensagens de texto."""
    
    body: str = Field(..., description="Conteúdo da mensagem de texto")


class Message(BaseModel):
    """Modelo para uma mensagem individual."""
    
    from_: str = Field(..., alias="from", description="Número do remetente")
    id: str = Field(..., description="ID único da mensagem")
    timestamp: str = Field(..., description="Timestamp da mensagem")
    type: str = Field(default="text", description="Tipo da mensagem")
    text: Optional[TextMessage] = Field(None, description="Conteúdo de texto (se aplicável)")


class ChatSession(BaseModel):
    """Modelo para uma sessão de chat."""
    
    user_id: str = Field(..., description="ID único do usuário")
    messages_count: int = Field(default=0, description="Número de mensagens na sessão")
    created_at: Optional[str] = Field(None, description="Data/hora de criação da sessão")


class AIResponse(BaseModel):
    """Modelo para resposta da IA."""
    
    status: str = Field(..., description="Status da resposta")
    message: str = Field(..., description="Mensagem de resposta")
    user_id: Optional[str] = Field(None, description="ID do usuário")
