"""
Módulo principal do aplicativo FastAPI.
Integração do WhatsApp com Google Gemini 2.5 Flash.

Este módulo coordena:
- Verificação do webhook do WhatsApp
- Recebimento e processamento de mensagens
- Integração com IA Gemini
- Envio de respostas via WhatsApp Cloud API
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_200_OK

from config import Config
from handlers.webhook_handler import verify_webhook, process_webhook
from services.gemini_client import ChatSessionManager
from services.meta_api import MetaAPIClient, WhatsAppMessageError
from typing import cast


# Inicialização da aplicação
app = FastAPI(
    title="CryptoLock Chatbot API",
    description="API de integração WhatsApp com Gemini AI",
    version="1.0.0"
)

# Validação de configuração na inicialização
try:
    Config.validate()
except EnvironmentError as e:
    raise RuntimeError(f"Falha na inicialização: {e}")

# Instância do gerenciador de sessões de chat
chat_manager = ChatSessionManager()

# Cliente da Meta API
try:
    meta_client = MetaAPIClient()
except WhatsAppMessageError as e:
    print(f"[WARNING] Cliente Meta API não inicializado: {e}")
    meta_client = None


# ============================================================================
# ROTAS DE WEBHOOK
# ============================================================================

@app.get("/webhook")
async def verify_webhook_endpoint(request: Request):
    """
Endpoint responsável por validar o webhook do WhatsApp junto à Meta.
Recebe os parâmetros de verificação pela URL, confirma o token e retorna
o challenge em texto puro, como a Meta exige para concluir a validação.
    """

    try:
        # Valida parâmetros e retorna o challenge
        challenge = await verify_webhook(request)

        # A Meta exige texto puro (sem JSON)
        return PlainTextResponse(content=challenge, status_code=200)

    except HTTPException:
        # Erros esperados (token inválido, parâmetros ausentes)
        raise

    except Exception as e:
        # Qualquer erro inesperado
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao verificar webhook")


@app.post("/webhook")
async def handle_webhook(data: dict):
    """
    Recebe e processa mensagens do WhatsApp.
    Integra com IA Gemini e envia respostas via WhatsApp Cloud API.
    
    Body:
        data: Dados do webhook da Meta
    
    Returns:
        dict: Status do processamento
    """
    try:
        # Processa os dados brutos do webhook
        webhook_data = await process_webhook(data)
        
        # Se não há mensagens ou é notificação de status, ignora
        if webhook_data.get("status") == "ignored":
            return {"status": "success", "message": "Evento ignorado"}
        
        # Se houve erro no processamento
        if webhook_data.get("status") == "error":
            print(f"[WARNING] Erro ao processar webhook: {webhook_data.get('detail')}")
            return {"status": "success", "message": "Webhook recebido"}
        
        # Extrai dados da mensagem
        sender_id = webhook_data.get("sender_id")
        message_type = webhook_data.get("message_type")
        raw_message = webhook_data.get("raw_message")
        
        # Processa mensagens de texto
        if message_type == "text" and raw_message:
            user_message = raw_message.get("text", {}).get("body", "")
            
            if not user_message or not sender_id:
                print("[WARNING] Mensagem ou ID do remetente vazio recebido")
                return {"status": "success", "message": "Mensagem vazia"}
            
            print(f"[INFO] Mensagem recebida de {sender_id}: {user_message}")
            
            # Obtém ou cria sessão de chat
            chat_session = chat_manager.get_or_create_session(str(sender_id))
            
            # Gera resposta com IA
            try:
                ai_response = chat_session.send_message(user_message)
            except Exception as e:
                print(f"[ERROR] Erro ao obter resposta do Gemini: {e}")
                ai_response = "Desculpe, ocorreu um erro ao processar sua mensagem."
            
            # Envia resposta via WhatsApp
            if meta_client:
                try:
                    meta_client.send_text_message(str(sender_id), ai_response)
                    print(f"[INFO] Resposta enviada para {sender_id}")
                except WhatsAppMessageError as e:
                    print(f"[ERROR] Falha ao enviar resposta: {e}")
            else:
                print("[WARNING] Cliente Meta API não disponível, resposta não enviada")
            
            return {"status": "success", "message": "Mensagem processada"}
        
        else:
            print(f"[INFO] Tipo de mensagem não suportado: {message_type}")
            return {"status": "success", "message": "Tipo de mensagem não suportado"}
    
    except Exception as e:
        print(f"[ERROR] Erro crítico ao processar webhook: {e}")
        # Retorna sucesso mesmo em erro para evitar retry do webhook
        return {"status": "success", "message": "Webhook recebido com erro"}


# ============================================================================
# ROTAS DE STATUS (Opcional - para monitoramento)
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Verifica a saúde da aplicação.
    
    Returns:
        dict: Status da aplicação
    """
    return {
        "status": "ok",
        "service": "CryptoLock Chatbot API",
        "active_sessions": len(chat_manager.sessions)
    }


@app.get("/status")
async def get_status():
    """
    Retorna informações sobre o estado da aplicação.
    
    Returns:
        dict: Informações de status detalhadas
    """
    return {
        "status": "running",
        "active_chat_sessions": len(chat_manager.sessions),
        "meta_client_available": meta_client is not None,
        "config_loaded": True
    }


# ============================================================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        reload=Config.DEBUG
    )
        


