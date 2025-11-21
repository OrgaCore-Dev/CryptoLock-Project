"""
Módulo de handlers.
Contém funções para processar diferentes tipos de requisições e webhooks.
"""

from .webhook_handler import verify_webhook, process_webhook

__all__ = ["verify_webhook", "process_webhook"]
