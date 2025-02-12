import requests
import os
import logging
from flask import Flask, request, jsonify

# Configuração do Flask
app = Flask(__name__)

# Configuração das variáveis de ambiente
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_KEY = os.getenv("NOTION_API_KEY")  # Chave da API do Notion
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")  # ID da página do Notion

# Configuração do Logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cabeçalhos para a requisição à API do Notion
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Função para adicionar uma tarefa no bloco de to-do
def adicionar_tarefa_to_do(titulo):
    data = {
        "parent": {"type": "page_id", "page_id": NOTION_PAGE_ID},
        "properties": {
            "title": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": titulo
                        }
                    }
                ]
            }
        }
    }

    logger.info(f"Enviando requisição para o Notion com o título: {titulo}")

    # Realiza a requisição à API do Notion
    response = requests.post(NOTION_API_URL, headers=HEADERS, json=data)

    # Log do status e resposta
    logger.debug(f"Status Code da requisição ao Notion: {response.status_code}")
    logger.debug(f"Resposta da API do Notion: {response.text}")

    try:
        return response.status_code, response.json()
    except requests.exceptions.JSONDecodeError:
        logger.error("Erro ao decodificar JSON. Resposta bruta:")
        logger.error(response.text)
        return response.status_code, {"erro": "Resposta inválida"}

# Rota para adicionar tarefa
@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.json
    logger.info(f"Dados recebidos: {data}")  # Log dos dados recebidos
    titulo = data.get('titulo')

    if not titulo:
        logger.warning("Erro: Título não fornecido")  # Log do erro de dados
        return jsonify({"erro": "Título não fornecido"}), 400

    status, resposta = adicionar_tarefa_to_do(titulo)
    logger.info(f"Status da requisição ao Notion: {status}")  # Log do status
    logger.info(f"Resposta do Notion: {resposta}")  # Log da resposta do Notion
    return jsonify({"status": status, "resposta": resposta}), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
