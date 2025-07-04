import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbLocal.db import session
from dbLocal.models import Tabela, Column


resultado = {}

tabelas = session.query(Tabela).all()
for tabela in tabelas:
    resultado[tabela.codigo] = {
        "descricao": tabela.descricao,
        "colunas": {
            coluna.codigo_coluna: coluna.descricao for coluna in tabela.colunas
        }
    }


CAMINHO_ARQUIVO = 'LoadData/schemas_tabelas.json'
with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)

print("JSON gerado com sucesso.")
