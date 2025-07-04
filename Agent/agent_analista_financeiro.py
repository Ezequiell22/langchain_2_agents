import os
import time
from dotenv import load_dotenv, find_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from openai import RateLimitError

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def AskAgentAnalist(dados: str, pergunta: str, tentativas: int = 3, espera_segundos: int = 2) -> str:
    """
    Gera um relatório analítico com base nos dados financeiros recebidos e na pergunta do usuário.

    :param dados: Dados em texto, tabela ou JSON retornado de uma consulta SQL.
    :param pergunta: A pergunta do usuário sobre os dados.
    :param tentativas: Número de tentativas caso ocorra erro de limite de uso.
    :param espera_segundos: Tempo entre as tentativas.
    :return: Relatório interpretativo em linguagem natural.
    """
    prompt = (
        "Você é um analista financeiro experiente. Abaixo estão os dados que você recebeu de um sistema ERP protheus:\n"
        f"{dados}\n"
        f"Com base nesses dados, responda à pergunta do usuário de forma clara, com análise e interpretação financeira:\n"
        f"{pergunta}\n"
        "Evite apenas repetir os dados. Responda resumidamente"
    )

    if not dados.strip():
        print("Não existem dados para serem analisados.")
        return "Não existem dados para serem analisados."
    elif dados.strip().lower().startswith("erro"):
        print("Algo deu errado na execução do sql")
        return "Algo deu errado na execução do sql"

    print("-> Prompt analista", prompt)

    for tentativa in range(1, tentativas + 1):
        try:
            
            with get_openai_callback() as cb:
                resposta = llm.invoke(prompt)
                print("\nResposta analista", resposta.content)
                print(f"\nTokens usados: {cb.total_tokens} | Custo estimado: ${cb.total_cost:.6f}")
                print(f"------------------------------------------------------------------------------")
                return resposta.content.strip()
        except RateLimitError as e:
            print(e)
            print(f"[Tentativa para o analista {tentativa}] Rate limit atingido. Aguardando {espera_segundos} segundos...")
            time.sleep(espera_segundos)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

    return "Erro ao gerar o relatório após múltiplas tentativas."
