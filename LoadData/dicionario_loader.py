import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from openai import OpenAI
from dbLocal.models import Tabela, Coluna 
from dbLocal.db import session
from dbSqlServer.db import engine

load_dotenv(find_dotenv())

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def perguntar_ao_chatgpt(pergunta: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em ERP Protheus e banco de dados. Responda em somente 3 a 4 palavras. Se precisar pesquise na web."},
                {"role": "user", "content": pergunta}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao perguntar ao ChatGPT: {e}")
        return "Descrição não disponível"

engine_sqlserver = engine

CODIGOS_TABELAS = ["SE1010", "SB1010", "SA1010", "SD1010", "SF2010", "SF1010", "SE2010"]  

def importar_schema(tabela_nome: str):
    try:    
        
        with engine_sqlserver.connect() as conn:
            query = text("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = :tabela
            """)
            result = conn.execute(query, {"tabela": tabela_nome})

            descricao_tabela = perguntar_ao_chatgpt(
                f"O que representa a tabela {tabela_nome} no ERP Protheus? Seja preciso no nome da tabela."
            )


            nova_tabela = Tabela(
                codigo=tabela_nome,
                descricao=descricao_tabela
            )
            session.add(nova_tabela)
            session.flush() 

            for row in result:
                codigo_coluna = row[0]
                descricao_coluna = perguntar_ao_chatgpt(
                    f"O que representa a coluna {codigo_coluna} da tabela {tabela_nome} no Protheus? Dê um nome descritivo e amigável."
                )
                nova_coluna = Coluna(
                    tabela_id=nova_tabela.id,
                    codigo_coluna=codigo_coluna,
                    descricao=descricao_coluna
                )
                session.add(nova_coluna)
                print(codigo_coluna, descricao_coluna )

            session.commit()
            print(f"Tabela {tabela_nome} e colunas salvas com sucesso.")

    except Exception as e:
        session.rollback()
        print(f"Erro ao importar {tabela_nome}: {e}")

def rodarTabelas():
    for tabela in CODIGOS_TABELAS:
        importar_schema(tabela)



