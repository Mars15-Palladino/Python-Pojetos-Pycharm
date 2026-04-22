

import pandas as pd
from tabulate import tabulate # Importa uma Vestimenta Bombada para as tabelas
import sqlite3
import os



def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
def Iniciar_Banco_De_Dados():
    try:
        conn = sqlite3.connect('Sistema de Financiamento de Veículos.db')
        print('.............Conectado ao Banco de Dados...........')
        cursor = conn.cursor()#cursor trabalhador. Ele que faz o trabalho de passar
                                # as informações pelo tunel

        cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes(ID INTEGER PRIMARY KEY AUTOINCREMENT,Nome TEXT NOT NULL,CPF TEXT NOT NULL UNIQUE,Sexo TEXT NOT NULL,Idade TEXT NOT NULL)''')
        print("Conexão estabelecida com sucesso", sqlite3.sqlite_version)
        conn.commit()
        print("Liberado para Uso")

        #CRIAÇÃO DO BANCO DOS VEÍCULOS
        cursor.execute('''CREATE TABLE IF NOT EXISTS Veiculos(ID INTEGER PRIMARY KEY AUTOINCREMENT, MARCA TEXT NOT NULL, MODELO TEXT NOT NULL,ANO INTEGER NOT NULL ,PLACA TEXT NOT NULL UNIQUE, ID_DONO INTEGER NOT NULL DEFAULT 1)''')
        conn.commit()
        return conn# Só pode ter um na sessão das tabelas

    except sqlite3.Error as erro:
        print("Erro",erro)
        return None
limpar_tela()
conexao = Iniciar_Banco_De_Dados()


def cadastra_Clientes(conn):
    try:
        print("="*45)
        print("Cadastro  de Clientes")
        print("="*45)
       # Transforma numa tabela usando o pandas, ele lê
       # o arquivo e faz tipo uma tabela do excel
    except sqlite3.Error as e:
        print("Erro ao listar",e)
    try:
        Nome = input("Insira o nome do cliente: ").strip()
        CPF = input("Insira o CPF do cliente: ").strip()
        Sexo = input("Insira o sexo do cliente M/F: ").strip().upper()# ponto upper, transforma em caixa alta
        Idade = input("Insira o Idade do cliente: ").strip()

        # 2. Faço para fazer a conexão no banco de dados
        cursor = conn.cursor()# Lembre-se do Alamo
        cursor.execute("INSERT INTO Clientes(Nome,CPF,Sexo,Idade) VALUES(?,?,?,?)",(Nome,CPF,Sexo,Idade))
        conn.commit()
        print("Cliente cadastrado com sucesso")
    except sqlite3.IntegrityError as erro1:
        print("Erro: CPF, já Cadastrado ",erro1)
    except sqlite3.Error as erro:
        print("Erro",erro)

def Listar_Clientes(conn):
    try:
        limpar_tela()
        #pd.set.option("display.max_colwidth",30)#limita nomes gigantes
        #pd.set_option("display.width",None)#Usa toda a largura do terminal
        #pd.set_option("display.colheader_justify","center")# Alihamento do título

        print("="*45)
        print("Lista de Clientes")
        print("="*45)
        df = pd.read_sql_query("SELECT * FROM Clientes", conn)# Transforma numa tabela usando o pandas, ele lê                                              # o arquivo e faz tipo uma tabela do excel
        if df.empty:
            print("Lista Vazia")
        else:
            print("="*45)
            # O 'headers' pega os nomes das colunas do banco
            # O 'tablefmt' define o desenho da tabela (o 'fancy_grid' é o mais bonito)
            #tabulete
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
            print("=" * 60)
        input("Aperte ENTER para voltar ao menu")
    except pd.io.sql.DatabaseError as erro_sql:
        # Este captura erros específicos do comando SQL (ex: nome da tabela errado)
        print(f"\n Erro de comando: Verifique se a tabela 'Clientes' existe. {erro_sql}")
    except sqlite3.Error as erro2_geral:
        print("Erro Inesperado",erro2_geral)

def deletar_Clientes(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("="*45)
        print("Deletar Clientes")
        print("="*45)
        ID_alvo = int(input("Insira o ID do cliente: "))
        if not ID_alvo:
            print("Nenhuma ID inserida")
            input("aperte ENTER para continuar OU voltar ao menu: ")
            return
        cursor.execute("SELECT Nome,CPF,Idade,Sexo FROM Clientes WHERE ID=?",(ID_alvo,))
        resultado = cursor.fetchone()
        print("Dados do cliente",resultado)
        if resultado:
            CPF_Alvo = resultado[0]
            Nome_alvo = resultado[1]
            Idade_alvo = resultado[2]
            Sexo_alvo= resultado[3]
            print("DADOS do cliente PARA EXCLUSÃO",CPF_Alvo,Nome_alvo,Idade_alvo,Sexo_alvo)
            print("-"*45)
            Confirmar = input("Tem Certeza que quer excluir S/N").upper()
            if Confirmar == "S":#Agora vamos para a parte que deleta
                cursor.execute("DELETE FROM Clientes WHERE ID=?",(ID_alvo,))
                conn.commit()
                print(
                    f"✅ Cliente Deletado: ID {ID_alvo} | Nome: {Nome_alvo} | CPF: {CPF_Alvo} | Idade: {Idade_alvo} | Sexo: {Sexo_alvo}")
            else:
                print("Nenhuma ID inserida: "+" Operação cancelada")
    except sqlite3.Error as erro:
        print("Nenhum Cliente Pertencente a essa ID",erro)

def alterar_Clientes(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("="*45)
        print("Alterar Clientes")
        print("="*45)
        ID_alvo = int(input("Insira o ID do cliente: "))
        if not ID_alvo:
            print("Nenhuma ID inserida")
            input("Aperte ENTER para continuar OU voltar ao menu: ")
            return
        cursor.execute("SELECT * FROM Clientes WHERE ID=?",(ID_alvo,))
        resultado = cursor.fetchone()
        conn.commit()
        print("Dados do Cliente",resultado)
        if resultado:
            CPF_Alvo = resultado[1]
            Nome_alvo = resultado[2]
            Idade_alvo = resultado[3]
            Sexo_alvo = resultado[4]
            print("Dados do Cliente para alteração", CPF_Alvo,Nome_alvo,Idade_alvo,Sexo_alvo )
            print("-"*45)
            Novo_Nome = input("Insira o nome do cliente: ").strip() or Nome_alvo
            Nova_Idade = input("Insira a Idade: ").strip() or Idade_alvo
            Novo_Sexo = input("Insira o Sexo: ").strip().upper() or Sexo_alvo

            confirmar = input("Tem Certeza que quer alterar S/N").upper().upper()
            if confirmar == "S": # Agora, a parte que alteramos
                cursor.execute("UPDATE Clientes SET Nome = ?,Sexo = ?,Idade = ? where ID=?",(Novo_Nome,Nova_Idade,Novo_Sexo, ID_alvo))# tem que seguir a mesma estrutura do principal
                conn.commit()
                print("Cliente alterado com sucesso")
            else:
                print("Operação cancelada")
        else:
            print("Nenhuma ID inserida")
    except ValueError as erro:
        print("Nenhuma ID inserida. Deve ser um Número",erro)
    except sqlite3.Error as erro:
        print("Nenhum Cliente Pertence a essa ID",erro)
    input("Aperte ENTER para continuar ou voltar ao menu: ")

    
while True:

        print("=" * 30)
        print("==========Menu Do Sistema=========")
        print("=" * 30)
        print("[1] Inserir dados")
        print("[2] Listar clientes")
        print("[3] alterar dados")
        print("[4] Deletar dados")
        print("[0] Sair")
        print("=" * 35)


        opcao = input("Escolha A Opção: ").strip()# .strip remove espaços vazios, antes  # e depois do que foi escrito

        match opcao:
            case "1":
             cadastra_Clientes(conexao)# aqui eu faço a conexão com a função cadastr clientes no Banco

            case "2":
                Listar_Clientes(conexao)#Aqui eu faço a listagem do que está armazenado
            case "3":
                alterar_Clientes(conexao)

            case "4":
                deletar_Clientes(conexao)

            case "0":
                limpar_tela()
                print("Saindo do sistema")
                conexao.close()
                break
            case _:
                print("Apenas opções Listadas")