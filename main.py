from Agent.agent_sql import AskAgent
from Agent.agent_analista_financeiro import AskAgentAnalist
from dbSqlServer.consultar import execute_sql

PERGUNTAS_TESTE = [
    'Quero o registro financeiro de maior valor?',
    'Quais os 10 produtos mais vendidos no mes de fevereiro?',
    'Quais os nomes e descrições das tabelas conhecidas?'
]

def executarPergunta(pergunta):
    print("************INICIO DO PROCESSO**************")
    Sql = AskAgent(pergunta, 2, 10)
    dados = execute_sql(Sql)
    respostaAgenteAnalista = AskAgentAnalist(dados, pergunta, 2, 30)
    print("************FIM DO PROCESSO**************")

def main():
    for pergunta in PERGUNTAS_TESTE:
        executarPergunta(pergunta)

if __name__ == "__main__":
    main()
