"""
Módulo de serviços.
Contém integrações com APIs externas (Gemini, Meta WhatsApp).
"""

from .gemini_client import ChatSessionManager, GeminiChatSession
from .meta_api import MetaAPIClient, send_whatsapp_message, WhatsAppMessageError

__all__ = [
    "ChatSessionManager",
    "GeminiChatSession",
    "MetaAPIClient",
    "send_whatsapp_message",
    "WhatsAppMessageError",
]
