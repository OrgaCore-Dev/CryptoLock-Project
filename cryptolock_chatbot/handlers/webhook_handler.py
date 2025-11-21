"""
Módulo para manipulação de webhooks do WhatsApp.
Responsável por processar requisições GET e POST do webhook.
"""

from fastapi import Request, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from config import Config


async def verify_webhook(request: Request) -> str:
    """
    Verifica o token de segurança da Meta para validar o webhook.
    
    Args:
        request: Objeto da requisição FastAPI.
        
    Returns:
        str: Challenge token se a verificação for bem-sucedida.
        
    Raises:
        HTTPException: Se o token for inválido ou parâmetros estiverem ausentes.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if not mode or not token:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Parâmetros ausentes: 'hub.mode' e 'hub.verify_token' são obrigatórios"
        )

    if mode == "subscribe" and token == Config.VERIFY_TOKEN:
        print("[INFO] Webhook verificado com sucesso")
        return challenge or ""
    
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Token de verificação inválido"
    )


async def process_webhook(data: dict) -> dict:
    """
    Processa dados recebidos do webhook do WhatsApp.
    Extrai informações da mensagem para processamento posterior.
    
    Args:
        data: Dicionário com dados do webhook.
        
    Returns:
        dict: Dicionário contendo informações extraídas ou aviso se sem mensagens.
    """
    try:
        # Extração segura dos dados da estrutura do webhook
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        # Ignora notificações de status
        if value.get("statuses"):
            return {"status": "ignored", "type": "status_notification"}

        messages = value.get("messages", [])
        if not messages:
            return {"status": "ignored", "type": "no_messages"}

        message = messages[0]
        sender_id = message.get("from")
        message_type = message.get("type")
        timestamp = message.get("timestamp")

        if not sender_id or not message_type:
            return {"status": "error", "detail": "Dados de mensagem incompletos"}

        return {
            "status": "success",
            "sender_id": sender_id,
            "message_type": message_type,
            "timestamp": timestamp,
            "raw_message": message
        }

    except (KeyError, IndexError, TypeError) as e:
        print(f"[ERROR] Erro ao processar webhook: {e}")
        return {"status": "error", "detail": str(e)}
