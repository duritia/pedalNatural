'''
Cria bancos de dados de teste - apaga os dados anteriores!
'''
import sqlite3                                  # Biblioteca de SQLite
import sys
from flask import Flask
from flask_cors import CORS

# Importa o arquivo com constantes para o projeto
import constantes

app = Flask(__name__)
CORS(app)

# Insere dados de teste nas tabelas
@app.route( "/populaParaTestes", methods=["GET"] )
def populaParaTestes() :
    '''
    Popula os bancos de dados com valores para teste
    '''

    # ==========================================================================
    # = = = = Popula banco das bicicletas:

    # create table bicicletas
    # (
    #     número          integer not null default 1 unique,
    #     situação        integer,
    #     estação         integer,
    #     destino         integer,
    #     alugadaEm       real,
    #     entregaMáxima   real,
    #     preço           real,
    #     primary key(número autoincrement)
    # );

    # Conecta ao banco de dados das bicicletas e insere dados nele
    conBicicletas = sqlite3.connect(".bancos/bicicletas")
    bdBicicletas = conBicicletas.cursor()
    print( "Conexão ao banco de bicicletas aberta." )

    dadosDeTeste = \
    [
        # número da bicicleta:          inteiro (chave do banco)
        # situação, estação, destino:   3 inteiros
        # alugada em, entrega máxima:   2 reais (data e hora SQLite)
        # preço do empréstimo:          real
        (
            None,                           # número da bicicleta
            constantes.BicicletaPronta,     # situação
            constantes.EstaçãoCentral,      # estação atual, quando guardada
            constantes.EstaçãoNãoDefinida,  # estação de destino, quando alugada

            # As datas de empréstimo e devolução serão dadas à função SQLite
            # julianday(), na hora de calcular o preço do aluguel.
            constantes.DataDesconsiderada,
            constantes.DataDesconsiderada,

            # Preço também é calculado na hora do aluguel
            0
        ),
        (
            None,
            constantes.BicicletaEmConserto, # situação
            constantes.EstaçãoNãoDefinida,  # estação atual, quando guardada
            constantes.EstaçãoVendaNova,    # estação de destino após o conserto

            # As datas de empréstimo e devolução serão dadas à função SQLite
            # julianday(), na hora de calcular o preço do aluguel.
            '2022-06-16 11:33:11',      # Momento em que vai pro conserto
            '2022-06-22 15:22:51',      # Previsão de devolução

            # Preço também é calculado na hora do aluguel
            0
        ),
        (
            None,
            constantes.BicicletaEstragada,      # situação
            constantes.EstaçãoNãoDefinida,      # estação atual, quando guardada
            constantes.EstaçãoSion,             # destino, quando estragada

            # As datas de empréstimo e devolução serão dadas à função SQLite
            # julianday(), na hora de calcular o preço do aluguel.
            '2022-02-01 10:11:01',      # Hora em que saiu para o conserto
            '2022-07-01 10:07:22',

            # Preço do conserto? Não pode ser definido quando ela sai, mas na
            # hora que ela volta, será colocada "pronta" para alugar. Então, o
            # preço de estragada não existe. Pra registrar o caixa, será feito
            # com a situação "em conserto", quando ela for devolvida.
            0
        ),
        (
            None,
            constantes.BicicletaAlugada,    # situação
            constantes.EstaçãoCentral,      # estação de onde foi emprestada
            constantes.EstaçãoPrado,        # estação de destino, quando alugada

            # As datas de empréstimo e devolução serão dadas à função SQLite
            # julianday(), na hora de calcular o preço do aluguel.
            '2022-02-02 20:02:22',
            '2022-07-01 11:22:11',

            # Preço a pagar, entregando dentro do prazo. Explicação didática no
            # arquivo
            # Para calcular este preço, fazemos a conta:
            # tempoDeAlguel * 24 * preçoPorHora
            # S
            0
        ),
        (
            None,
            constantes.BicicletaNãoDevolvida,   # situação
            constantes.EstaçãoCentral,      # estação de onde foi emprestada
            constantes.EstaçãoPrado,        # estação de destino, quando alugada

            # As datas de empréstimo e devolução serão dadas à função SQLite
            # julianday(), na hora de calcular o preço do aluguel.
            '2022-02-02 20:02:22',
            '2022-07-01 10:07:22',

            # Preço também é calculado na hora do aluguel
            0
        )
    ]

    try:
        # Apaga todos os dados da tabela, se existirem
        bdBicicletas.execute( "delete from bicicletas" )

        # Insere os dados das bicicletas
        bdBicicletas.executemany \
        (
            "insert into bicicletas values ( ?, ?, ?, ?, ?, ?, ?)",
            dadosDeTeste
        )
        print( "Pedidos para inserção de bicicletas terminados." )

        conBicicletas.commit()
        print( "Confirmação das inserções feita." )

        conBicicletas.close()
        print( "Banco de bicicletas fechado." )
        #return "Inserções no banco feitas e confirmadas."

    except:
        print( "Erro ao inserir bicicletas de teste." )
        conBicicletas.close()

        # Imprime de forma "crua" a saída da função exc_info()
        print( sys.exc_info() )

        # Imprime de forma amigável e informativa os dados exceção acontecida
        sys.excepthook( *sys.exc_info() )

        return "Erro ao inserir bicicletas de teste."

    # ==========================================================================
    # = = = = Popula banco dos usuários:

    # create table usuários
    # (
    #     cpf               integer not null unique,
    #     senha             text,
    #     nome              text,
    #     logradouro        text,
    #     número            integer,
    #     complemento       text,
    #     bairro            text,
    #     cep               integer,
    #     cidade            text,
    #     estado            text,
    #     cartãoDeCrédito1  integer,
    #     bandeiraCartão1   integer,
    #     bancoDaConta1     integer,
    #     agênciaConta1     integer,
    #     operaçãoConta1    integer,
    #     númeroConta1      integer,
    #     primary key (cpf)
    # );

    # Conecta ao banco de dados dos usuários e insere dados nele
    conUsuários = sqlite3.connect(".bancos/usuários")
    bdUsuários = conUsuários.cursor()
    print( "Conexão ao banco de usuários aberta." )

    dadosDeTeste = \
    [
        # CPF                       inteiro (chave do banco)
        # senha                     texto (3x)
        # nome completo             texto
        # logradouro                texto
        # número                    inteiro
        # complemento               texto (2x)
        # bairro                    texto
        # CEP                       inteiro
        # cidade                    texto (2x)
        # estado (sigla)            texto
        # cartão de crédito #1      inteiro (6x)
        # bandeira do cartão #1     inteiro (tabela)
        # nome do banco da conta #1 inteiro (tabela)
        # agência da conta #1       inteiro
        # operação da conta #1      inteiro
        # número da conta #1        inteiro
        (
            1,
            "123456",
            "Maria José da Silva",
            "rua xerentes",
            31,
            "",
            "Santa Mônica",
            31530170,
            "Belo Horizonte",
            "MG",
            12341234,
            0,
            0,
            123,
            0,
            5307013
        ),
        (
            2,
            "123456",
            "José Maria da Silva",
            "rua xerentes",
            31,
            "",
            "Santa Mônica",
            31530170,
            "Belo Horizonte",
            "MG",
            56785678,
            0,
            0,
            123,
            0,
            1230803
        ),
        (
            3,
            "123456",
            "Joaquim José da Silva Xavier",
            "rua tiradentes",
            333,
            "",
            "Incipit Vita Nova",
            35250130,
            "Curvelo",
            "MG",
            54546565,
            0,
            0,
            234,
            0,
            1209087
        ),
        (
            4,
            "123456",
            "Rosângela da Silva",
            "rua dos peixes",
            12,
            "",
            "Monte Grande",
            10120130,
            "União da Vitória",
            "PR",
            43214321,
            0,
            0,
            13,
            0,
            83073
        )
    ]

    # Laço para inserir os dados
    try:
        # Apaga todos os dados da tabela, se existirem
        bdUsuários.execute( "delete from usuários" )

        bdUsuários.executemany \
        (
            # São 16 campos para inserir
            "insert into usuários values \
            ( \
                ?, ?, ?, ?, ?, \
                ?, ?, ?, ?, ?, \
                ?, ?, ?, ?, ?, \
                ? \
            )",
            dadosDeTeste
        )
        print( "Pedidos para inserção de usuários terminados." )

        conUsuários.commit()
        print( "Confirmação das inserções terminada." )

        conUsuários.close()
        print( "Banco de usuários fechado." )
        #return "Inserções no banco feitas e confirmadas."

    except:
        print( "Erro ao inserir usuários de teste." )
        conUsuários.close()

        # Imprime de forma "crua" a saída da função exc_info()
        print( sys.exc_info() )

        # Imprime de forma amigável e informativa os dados exceção acontecida
        sys.excepthook( *sys.exc_info() )

        return "Erro ao inserir usuários de teste."

    # ==========================================================================
    # = = = = Popula banco das estações:

    # create table estações
    # (
    #     númestação          integer not null unique,
    #     capacidade          integer,
    #     vagas               integer,
    #     chegadadebicicleta  real,
    #     logradouro          text,
    #     número              integer,
    #     complemento         text,
    #     bairro              text,
    #     cep                 integer,
    #     cidade              text,
    #     estado              text,
    #     referência1         text,
    #     referência2         text,
    #     referência3         text,
    #     referência4         text,
    #     primary key(númestação autoincrement)
    # )

    # Conecta ao banco de dados dos usuários e insere dados nele
    conEstações = sqlite3.connect(".bancos/estações")
    bdEstações = conEstações.cursor()
    print( "Conexão ao banco de estações aberta." )

    dadosDeTeste = \
    [
        # número da estação       inteiro (chave do banco)
        # capacidade              inteiro (2x)
        # vagas (no momento)      inteiro
        # chegada de bicicleta    real (data e hora)
        # logradouro              texto
        # número                  inteiro
        # complemento             texto (2x)
        # bairro                  texto
        # CEP                     inteiro
        # cidade                  texto (6x)
        # estado (sigla)          texto
        # referência #1           texto
        # referência #2           texto
        # referência #3           texto
        # referência #4           texto
        (
            None,
            30,
            0,
            constantes.DataDesconsiderada,
            "rua Rio de Janeiro",
            21,
            "",
            "Centro",
            31144113,
            "Belo Horizonte",
            "MG",
            "Entre ruas dos aimorés e rua dos incas",
            "Em frente à prefeitura",
            "",
            ""
        ),
        (
            None,
            30,
            0,
            constantes.DataDesconsiderada,
            "avenida padre pedro pinto",
            321,
            "",
            "Venda Nova",
            31420130,
            "Belo Horizonte",
            "MG",
            "entre rua alberto siqueira e rua guilherme arantes",
            "em frente à UPA Venda Nova",
            "",
            ""
        )
    ]

    # Laço para inserir os dados
    try:
        # Apaga todos os dados da tabela, se existirem
        bdEstações.execute( "delete from estações" )

        bdEstações.executemany \
        (
            # São 15 campos para inserir
            "insert into estações values \
            ( \
                ?, ?, ?, ?, ?, \
                ?, ?, ?, ?, ?, \
                ?, ?, ?, ?, ?  \
            )",
            dadosDeTeste
        )
        print( "Pedidos para inserção de estações terminados." )

        conEstações.commit()
        print( "Confirmação das inserções terminada." )

        conEstações.close()
        print( "Banco de estações fechado." )
        #return "Inserções no banco feitas e confirmadas."

    except:
        print( "Erro ao inserir estações de teste." )
        conEstações.close()

        # Imprime de forma "crua" a saída da função exc_info()
        print( sys.exc_info() )

        # Imprime de forma amigável e informativa os dados exceção acontecida
        sys.excepthook( *sys.exc_info() )

        return "Erro ao inserir usuários de teste."

    return "populaParaTestes terminada"

# Executa o arquivo e fica pronto para a chamada de /populaParaTestes localmente
@app.run()
def nada() :
    ''' Função adicionada apenas para que o código seja válido '''
    print( "Nada é executada?" )
    return "Nada"

# vim: fileencoding=utf-8: expandtab: shiftwidth=4: tabstop=8: softtabstop=4
