"""
Módulo de configuração centralizada da aplicação.
Gerencia variáveis de ambiente e constantes do projeto.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    """Classe para armazenar configurações da aplicação."""
    
    # Variáveis de ambiente críticas
    VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
    
    # URLs de API
    WHATSAPP_API_BASE_URL = "https://graph.facebook.com/v19.0"
    
    # Modelo de IA padrão
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Configuração do servidor
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 8000
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Valida se todas as variáveis críticas estão configuradas."""
        required_vars = [
            ("VERIFY_TOKEN", cls.VERIFY_TOKEN),
            ("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            ("WHATSAPP_API_TOKEN", cls.WHATSAPP_API_TOKEN),
            ("PHONE_NUMBER_ID", cls.PHONE_NUMBER_ID),
        ]
        
        missing_vars = [name for name, value in required_vars if not value]
        
        if missing_vars:
            raise EnvironmentError(
                f"Variáveis de ambiente obrigatórias não configuradas: {', '.join(missing_vars)}. "
                "Verifique o arquivo .env e a instalação do python-dotenv."
            )
    
    @classmethod
    def get_whatsapp_api_url(cls) -> str:
        """Retorna a URL completa da Meta WhatsApp API para enviar mensagens."""
        return f"{cls.WHATSAPP_API_BASE_URL}/{cls.PHONE_NUMBER_ID}/messages"
