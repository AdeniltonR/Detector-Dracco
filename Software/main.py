"""
 * NOME: Adenilton Ribeiro
 * DATA: 20/03/2026
 * PROJETO: Sistema de Detector de Dracco
 * VERSAO: 1.0.0
 * DESCRICAO: - 
"""
from src.web.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)