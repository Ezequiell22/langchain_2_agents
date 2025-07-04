from dbLocal.models import Tabela, Coluna 
from dbLocal.db import session

def AtualizarDescricaoTabelas():
    novas_descricoes = {
        "SE1010": "Cadastro de transportadoras ",
        "SB1010": "Cadastro de produtos ",
        "SA1010": "Cadastro de clientes ",
        "SD1010": "Cadastro de fornecedores com dados fiscais e de contato.",
        "SF1010": "Cabeçalho das notas fiscais",
        "SF2010": "Itens das notas fiscais",
        "SE2010": "Conhecimentos de transporte"
    }

    for codigo, nova_descricao in novas_descricoes.items():
        tabela = session.query(Tabela).filter_by(codigo=codigo).first()
        if tabela:
            tabela.descricao = nova_descricao
            print(f"✔️ Atualizado: {codigo}")
        else:
            print(f"⚠️ Tabela {codigo} não encontrada no banco.")


    session.commit()
    session.close()
