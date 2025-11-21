"""
Módulo de integração com Google Gemini AI.
Responsável pela comunicação com a API do Gemini e gerenciamento de sessões de chat.
"""

from typing import Optional
from google import genai

from config import Config


class GeminiChatSession:
    """Gerencia uma sessão de chat com o Gemini AI."""
    
    def __init__(self, user_id: str, system_instruction: Optional[str] = None):
        """
        Inicializa uma nova sessão de chat.
        
        Args:
            user_id: ID único do usuário.
            system_instruction: Instrução de sistema personalizada para o chat.
        """
        self.user_id = user_id
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        default_instruction = (
            "Você é um assistente virtual amigável e prestativo para um projeto de faculdade. "
            "Mantenha as respostas concisas e no máximo 3 frases."
        )
        
        system_instruction = system_instruction or default_instruction
        
        self.chat = self.client.chats.create(
            model=Config.GEMINI_MODEL,
            config={"system_instruction": system_instruction}
        )
    
    def send_message(self, message: str) -> str:
        """
        Envia uma mensagem para o Gemini e retorna a resposta.
        
        Args:
            message: Conteúdo da mensagem do usuário.
            
        Returns:
            str: Resposta do Gemini AI.
            
        Raises:
            Exception: Se houver erro na comunicação com a API.
        """
        try:
            response = self.chat.send_message(message)
            return response.text or ""
        except Exception as e:
            print(f"[ERROR] Erro ao comunicar com Gemini para usuário {self.user_id}: {e}")
            raise


class ChatSessionManager:
    """Gerencia múltiplas sessões de chat de diferentes usuários."""
    
    def __init__(self):
        """Inicializa o gerenciador de sessões."""
        self.sessions: dict[str, GeminiChatSession] = {}
    
    def get_or_create_session(self, user_id: str, system_instruction: Optional[str] = None) -> GeminiChatSession:
        """
        Obtém uma sessão existente ou cria uma nova para o usuário.
        
        Args:
            user_id: ID único do usuário.
            system_instruction: Instrução de sistema personalizada (usado na criação).
            
        Returns:
            GeminiChatSession: Sessão de chat do usuário.
        """
        if user_id not in self.sessions:
            self.sessions[user_id] = GeminiChatSession(user_id, system_instruction)
            print(f"[INFO] Nova sessão de chat criada para usuário {user_id}")
        
        return self.sessions[user_id]
    
    def get_session(self, user_id: str) -> Optional[GeminiChatSession]:
        """
        Obtém uma sessão existente sem criar uma nova.
        
        Args:
            user_id: ID único do usuário.
            
        Returns:
            GeminiChatSession ou None: Sessão se existir, None caso contrário.
        """
        return self.sessions.get(user_id)
    
    def delete_session(self, user_id: str) -> bool:
        """
        Deleta uma sessão de chat.
        
        Args:
            user_id: ID único do usuário.
            
        Returns:
            bool: True se deletada, False se não existia.
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
            print(f"[INFO] Sessão de chat deletada para usuário {user_id}")
            return True
        return False
    
    def clear_all_sessions(self):
        """Limpa todas as sessões de chat."""
        self.sessions.clear()
        print("[INFO] Todas as sessões de chat foram limpas")
