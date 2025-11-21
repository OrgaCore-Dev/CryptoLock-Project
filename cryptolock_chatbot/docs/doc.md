# Projeto: Automação de Comunicação com IA

## Informação Básica
- Objetivo: Desenvolver um chatbot para WhatsApp que usa IA para respostas inteligentes e contextuais.
- Linguagem principal: Python 3.x
- Público-alvo: Clientes que interagem com a empresa via WhatsApp
- Status: Em Desenvolvimento 🚀

---

## Stack Tecnológico (visão geral)
Arquitetura em microsserviços e APIs, integrando a Cloud API do WhatsApp (Meta) com a Gemini API (Google). Backend assíncrono em FastAPI.

### 1. Backend e Infraestrutura
- Python
    - Linguagem principal, extensas bibliotecas para IA (SDK google-genai).
- FastAPI
    - Servidor web assíncrono para receber webhooks do WhatsApp e orquestrar chamadas à IA.
    - Justificativa: alto desempenho e código conciso.
- Uvicorn
    - ASGI server recomendado para produção/testes.

### 2. Conexão e Comunicação (WhatsApp)
- Cloud API do WhatsApp (Meta)
    - Canal oficial para envio/recebimento de mensagens.
    - Vantagem: estabilidade, conformidade e camada gratuita inicial (1.000 conversas/mês).
- Webhook
    - Endpoint: POST /webhook no FastAPI para receber JSON das mensagens.
    - Modelo assíncrono exigido pela Meta.
- Ngrok / Cloudflare Tunnel
    - Ferramentas para expor o servidor local durante desenvolvimento e testes.

### 3. Inteligência Artificial
- Gemini API (Google)
    - Processamento de linguagem natural e geração de respostas.
    - Modelo sugerido: Gemini 2.5 Flash (bom trade-off entre velocidade e qualidade).
    - Camada gratuita generosa (Free Tier).
- SDK Python (google-genai)
    - Biblioteca oficial para chamadas ao serviço e gerenciamento de sessões/prompt.
- Prompt Engineering
    - Definir System Prompt (persona, tom de voz, instruções de atendimento).

---

## Vantagens e Benefícios
- Baixo custo operacional: camadas gratuitas da Cloud API e Gemini reduzem despesas.
- Estabilidade e confiabilidade: uso de APIs oficiais e frameworks modernos diminui risco operacional.
- Alta inteligência: modelos otimizados para conversação melhoram entendimento de contexto.
- Desenvolvimento rápido: Python + FastAPI + SDK google-genai aceleram a implementação.

---

## Fluxo de Dados (Arquitetura) — passo a passo
1. Mensagem Recebida (WhatsApp → FastAPI)
     - Cliente envia mensagem ao número Business.
     - A Cloud API formata e envia JSON ao endpoint /webhook do FastAPI.
2. Processamento da IA (FastAPI → Gemini)
     - FastAPI extrai texto e ID do remetente do JSON.
     - Chamada assíncrona à Gemini API com mensagem e histórico (se aplicável).
     - Gemini retorna resposta de texto.
3. Resposta Enviada (FastAPI → WhatsApp)
     - FastAPI recebe a resposta da Gemini.
     - Envia POST à Cloud API da Meta com número do cliente e texto gerado.
     - Cloud API entrega a resposta ao cliente no WhatsApp.

---

## Próximos Passos sugeridos
- Definir e testar System Prompt (persona do bot).
- Implementar endpoint /webhook e flow assíncrono com FastAPI + Uvicorn.
- Integrar SDK google-genai e criar handlers de sessão/historico.
- Configurar e testar Cloud API do WhatsApp (conta, credenciais e webhooks).
- Testes locais com ngrok / Cloudflare Tunnel e testes de carga iniciais.

---

## Observações
- Priorizar uso das APIs oficiais para evitar bloqueios e problemas legais.
- Monitorar consumo das camadas gratuitas para ajustes de custo.
- Logar conversas e erros de forma segura (atenção a dados sensíveis).
- Planejar fallback/timeout para chamadas à API de IA em caso de indisponibilidade.
