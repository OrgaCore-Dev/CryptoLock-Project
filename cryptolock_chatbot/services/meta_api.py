"""
Módulo de integração com Meta WhatsApp Cloud API.
Responsável pelo envio de mensagens via WhatsApp.
"""

import requests
from typing import Optional

from config import Config


class WhatsAppMessageError(Exception):
    """Exceção para erros ao enviar mensagens via WhatsApp."""
    pass


class MetaAPIClient:
    """Cliente para integração com Meta WhatsApp Cloud API."""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Inicializa o cliente da Meta API.
        
        Args:
            api_token: Token de acesso da API (usa Config.WHATSAPP_API_TOKEN se não fornecido).
        """
        self.api_token = api_token or Config.WHATSAPP_API_TOKEN
        self.api_url = Config.get_whatsapp_api_url()
        
        if not self.api_token:
            raise WhatsAppMessageError("Token da WhatsApp Cloud API não configurado")
    
    def _get_headers(self) -> dict:
        """
        Retorna os headers padrão para requisições à API.
        
        Returns:
            dict: Headers com autenticação e tipo de conteúdo.
        """
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, recipient_id: str, text: str) -> dict:
        """
        Envia uma mensagem de texto via WhatsApp.
        
        Args:
            recipient_id: Número do destinatário (com código do país).
            text: Conteúdo da mensagem.
            
        Returns:
            dict: Resposta da API com ID da mensagem.
            
        Raises:
            WhatsAppMessageError: Se houver erro ao enviar a mensagem.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "text": {"body": text}
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"[INFO] Mensagem enviada para {recipient_id}: {text}")
            return result
            
        except requests.exceptions.HTTPError as e:
            error_detail = response.text if response else str(e)
            print(f"[ERROR] Erro HTTP ao enviar mensagem para {recipient_id}: {error_detail}")
            raise WhatsAppMessageError(f"Erro ao enviar mensagem: {error_detail}") from e
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Erro de conexão ao enviar mensagem para {recipient_id}: {e}")
            raise WhatsAppMessageError(f"Erro de conexão: {e}") from e
        
        except (ValueError, KeyError) as e:
            print(f"[ERROR] Erro ao processar resposta da API: {e}")
            raise WhatsAppMessageError(f"Resposta inválida da API: {e}") from e


def send_whatsapp_message(
    recipient_id: str,
    text: str,
    api_url: Optional[str] = None,
    token: Optional[str] = None
) -> bool:
    """
    Função auxiliar para compatibilidade com código legado.
    Envia uma mensagem de texto via WhatsApp usando a MetaAPIClient.
    
    Args:
        recipient_id: Número do destinatário.
        text: Conteúdo da mensagem.
        api_url: URL da API (ignorado, usa Config.get_whatsapp_api_url()).
        token: Token de acesso (usa Config.WHATSAPP_API_TOKEN se não fornecido).
        
    Returns:
        bool: True se enviado com sucesso, False caso contrário.
    """
    try:
        client = MetaAPIClient(api_token=token)
        client.send_text_message(recipient_id, text)
        return True
    except WhatsAppMessageError as e:
        print(f"[ERROR] {e}")
        return False
