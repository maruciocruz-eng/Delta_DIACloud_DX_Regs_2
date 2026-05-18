from flask import Flask, jsonify, request
from requests.auth import HTTPBasicAuth
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Credenciais no arquivo .env (NUNCA no código)
API_URL = "https://api.diacloudsolutions.com/devices/82259/regs"
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")

# Cache para evitar múltiplas requisições
dados_cache = None
cache_timestamp = None

@app.route('/api/dados', methods=['GET'])
def obter_dados():
    """Busca dados da API Diacloud"""
    try:
        resposta = requests.get(
            API_URL,
            auth=HTTPBasicAuth(API_USER, API_PASS),
            timeout=5
        )
        resposta.raise_for_status()
        
        dados = resposta.json()
        lista_dados = dados.get("data", [])
        
        # Retorna apenas informações essenciais (addr e value)
        dados_simplificados = [
            {"index": i, "addr": item['addr'], "value": item['value']}
            for i, item in enumerate(lista_dados)
        ]
        
        return jsonify({"sucesso": True, "dados": dados_simplificados})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

@app.route('/api/item/<int:indice>', methods=['GET'])
def obter_item(indice):
    """Retorna um item específico da lista"""
    try:
        resposta = requests.get(
            API_URL,
            auth=HTTPBasicAuth(API_USER, API_PASS),
            timeout=5
        )
        resposta.raise_for_status()
        
        dados = resposta.json()
        lista_dados = dados.get("data", [])
        
        # Validação do índice
        if indice < 0 or indice >= len(lista_dados):
            return jsonify({"sucesso": False, "erro": "Índice fora do intervalo"}), 400
        
        item = lista_dados[indice]
        return jsonify({
            "sucesso": True,
            "indice": indice,
            "addr": item['addr'],
            "value": item['value']
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

@app.route('/')
def index():
    """Página principal"""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)