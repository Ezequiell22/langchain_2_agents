from langchain.agents import  Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from myTools.sql_tools import traduzir_sql, consultar_dicionario
import os
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.prompts import ChatPromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
import time
from openai import RateLimitError
from dbSqlServer.db import connection_string

_ = load_dotenv(find_dotenv())

db = SQLDatabase.from_uri(
    connection_string,
    include_tables=["SE1010", "SB1010", "SA1010", "SD1010", "SF2010", "SF1010", "SE2010"],
    engine_args={"echo": False},
    sample_rows_in_table_info=0
)

llm = ChatOpenAI(temperature=0, model="gpt-4o")


def executar_sql_com_traducao(query: str) -> str:
    try:
        query_traduzida = traduzir_sql(query)
        print(f"\nConsulta original: {query}")
        print(f"Consulta traduzida: {query_traduzida}")
        resultados = db.run(query_traduzida)
        return (
                f"Resultado da consulta SQL:\n{resultados}\n\n"
                f"sql: "
            )
    except Exception as e:
        return f"Erro ao executar a query: {str(e)}"


tools = [
    Tool(
        name="sql_db_query",
        func=executar_sql_com_traducao,
        description="Use esta ferramenta para EXECUTAR consultas SQL e OBTER os resultados reais do banco, não apenas gerar o SQL."
    ),
    
    # Tool(
    # name="consultar_dicionario",
    # func=consultar_dicionario,
    # description=(
    #     "Use esta ferramenta para descobrir o nome real de tabelas ou colunas usando palavras comuns como 'endereço', 'cliente', etc. "
    #     "Ela retorna os nomes codificados a partir de termos legíveis."
    # )
    #)

]


sql_agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm, tools=tools),
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=False
)


def AskAgent(strAsk : str, tentativas: int = 3, espera_segundos: int = 0) -> str:
    """
    Faz uma pergunta ao agente com retry e espera, em caso de erro de limite de taxa.

    :param pergunta: Texto da pergunta para o agente
    :param tentativas: Número de tentativas em caso de erro
    :param espera_segundos: Tempo de espera entre tentativas (em segundos)
    :return: Resposta do agente ou mensagem de erro
    """

    prompt_sql = (
            f"Voce é um especialista em sql do ERP protheus."
            f"Gere apenas o SQL necessário, sem usar markdown, sem ```sql. "
            f"sem nenhum texto explicativo antes. Apenas a instrução SQL limpa. "
            f"Voce não deve executar o sql, apenas gerar o sql."
            f"Se não souber responder, diga: 'Desculpe, não sei.' "
            f"Pergunta: {strAsk}"
        )
    
    for tentativa in range(1, tentativas + 1):
        try:
            
            with get_openai_callback() as cb:

                respostaAgenteSql = sql_agent.invoke({"input": prompt_sql}, callbacks=[cb])
                print("\nResposta agente sql:\n", respostaAgenteSql['output'])
                print(f"\nTokens usados: {cb.total_tokens} | Custo estimado: ${cb.total_cost:.6f}")
                print(f"------------------------------------------------------------------------------")

                return respostaAgenteSql['output']

        except RateLimitError as e:
            print(e)
            print(f"[Tentativa para o agente de sql {tentativa}] Rate limit atingido. Aguardando {espera_segundos} segundos...")
            time.sleep(espera_segundos)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

    return "Erro ao consultar agente sql após múltiplas tentativas."

