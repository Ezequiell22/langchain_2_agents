import pandas as pd
from sqlalchemy import create_engine, text
import time
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote_plus
import os

_ = load_dotenv(find_dotenv())

odbc_str = (
    f"DRIVER={os.getenv('ODBC_DRIVER')};"
    f"SERVER={os.getenv('SERVER_DB')};"
    f"DATABASE={os.getenv('DATABASE')};"
    f"UID={os.getenv('USER_DB')};"
    f"PWD={os.getenv('PASS_DB')};"
    f"TrustServerCertificate=yes;"
)
quoted = quote_plus(odbc_str)
connection_string = f"mssql+pyodbc:///?odbc_connect={quoted}"

engine = create_engine(connection_string, echo=False)


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
