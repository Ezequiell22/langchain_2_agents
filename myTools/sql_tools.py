import re
import json
import re
from dbLocal.db import session
from dbLocal.models import Tabela, Coluna

def traduzir_sql(sql: str) -> str:
    print('>>> traduzir_sql')

    tabelas = session.query(Tabela).all()
    for tabela in tabelas:
        if tabela.descricao.lower() in sql.lower():
            sql = re.sub(
                rf'\b{re.escape(tabela.descricao)}\b',
                tabela.codigo,
                sql,
                flags=re.IGNORECASE
            )

    colunas = session.query(Coluna).all()
    for coluna in colunas:
        if coluna.descricao.lower() in sql.lower():
            sql = re.sub(
                rf'\b{re.escape(coluna.descricao)}\b',
                coluna.codigo,
                sql,
                flags=re.IGNORECASE
            )

    print('>>> SQL traduzido:', sql)
    return sql



def consultar_dicionario(entrada: str) -> str:
    entrada = entrada.lower()
    resultados = []

    tabelas = session.query(Tabela).filter(Tabela.descricao.ilike(f"%{entrada}%")).all()

    for tabela in tabelas:
        resultados.append(f"Tabela: {tabela.descricao} (Código: {tabela.codigo})")

        colunas = session.query(Coluna).filter(Coluna.tabela_id == tabela.codigo).all()
        for coluna in colunas:
            resultados.append(f"  Coluna: {coluna.descricao} (Código: {coluna.codigo})")

    if not resultados:
        return f"Nenhuma correspondência encontrada para '{entrada}'."

    print('resultados', resultados)
    return "\n".join(resultados)
