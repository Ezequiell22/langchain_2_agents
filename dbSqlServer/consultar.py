import pandas as pd
from sqlalchemy import  text
import time
from dbSqlServer.db import engine

def execute_sql(sql: str) -> str:
    """
    Executa um comando SQL no banco configurado e retorna os dados formatados em Markdown.
    """
    if not sql.strip().lower().startswith("select"):
        return "Erro. Somente consultas SELECT são permitidas."
    
    try:
        start_time = time.time()

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

        df = pd.DataFrame(rows, columns=columns)
        elapsed = round(time.time() - start_time, 2)
        print(f"Tempo de consulta SQL: {elapsed} s")

        if df.empty:
            return("Erro. A consulta foi executada com sucesso, mas não retornou nenhum dado.")

        tabela_formatada = df.to_markdown(index=False)
        print(f"Dados", tabela_formatada)
        return tabela_formatada

    except Exception as e:
        print( f"Erro ao executar a consulta SQL: {str(e)}")
        return ''
