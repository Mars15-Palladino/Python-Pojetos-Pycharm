from unittest import result

import pandas as pd
from tabulate import tabulate  # Importa uma Vestimenta Bombada para as tabelas
import sqlite3
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def Iniciar_Banco_De_Dados():
    try:
        conn = sqlite3.connect('Sistema de Financiamento de Veículos.db')
        print('.............Conectado ao Banco de Dados...........')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes
                          (
                              ID
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT,
                              Nome
                              TEXT
                              NOT
                              NULL,
                              CPF
                              TEXT
                              NOT
                              NULL
                              UNIQUE,
                              Sexo
                              TEXT
                              NOT
                              NULL,
                              Idade
                              TEXT
                              NOT
                              NULL
                          )''')
        print("Conexão estabelecida com sucesso", sqlite3.sqlite_version)
        conn.commit()
        print("Liberado para Uso")

        cursor.execute('''CREATE TABLE IF NOT EXISTS Veiculos
                          (
                              ID
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT,
                              MARCA
                              TEXT
                              NOT
                              NULL,
                              MODELO
                              TEXT
                              NOT
                              NULL,
                              ANO
                              INTEGER
                              NOT
                              NULL,
                              PLACA
                              TEXT
                              NOT
                              NULL
                              UNIQUE,
                              ID_DONO
                              INTEGER
                              NOT
                              NULL
                          )''')
        conn.commit()
        return conn

    except sqlite3.Error as erro:
        print("Erro", erro)
        return None


limpar_tela()
conexao = Iniciar_Banco_De_Dados()


def cadastra_Clientes(conn):
    print("=" * 45)
    print("Cadastro  de Clientes")
    print("=" * 45)

    try:
        Nome = input("Insira o nome do cliente: ").strip()
        CPF = input("Insira o CPF do cliente: ").strip()
        Sexo = input("Insira o sexo do cliente M/F: ").strip().upper()

        # PROTEÇÃO IDADE
        while True:
            Idade = input("Insira o Idade do cliente: ").strip()
            if Idade.isdigit(): break
            print("⚠️ Erro: Digite apenas números para a idade!")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Clientes(Nome,CPF,Sexo,Idade) VALUES(?,?,?,?)", (Nome, CPF, Sexo, Idade))
        conn.commit()
        print("Cliente cadastrado com sucesso")
    except sqlite3.IntegrityError as erro1:
        print("Erro: CPF, já Cadastrado ", erro1)
    except sqlite3.Error as erro:
        print("Erro", erro)


def Listar_Clientes(conn):
    try:
        limpar_tela()
        print("=" * 45)
        print("Lista de Clientes")
        print("=" * 45)
        df = pd.read_sql_query("SELECT * FROM Clientes", conn)
        if df.empty:
            print("Lista Vazia")
        else:
            print("=" * 45)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
            print("=" * 60)
        input("Aperte ENTER para voltar ao menu")
    except pd.io.sql.DatabaseError as erro_sql:
        print(f"\n Erro de comando: Verifique se a tabela 'Clientes' existe. {erro_sql}")
    except sqlite3.Error as erro2_geral:
        print("Erro Inesperado", erro2_geral)


def deletar_Clientes(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("=" * 45)
        print("Deletar Clientes")
        print("=" * 45)

        # PROTEÇÃO ID
        while True:
            entrada = input("Insira o ID do cliente: ").strip()
            if entrada.isdigit():
                ID_alvo = int(entrada)
                break
            print("⚠️ Erro: O ID deve ser um número!")

        cursor.execute("SELECT Nome,CPF,Idade,Sexo FROM Clientes WHERE ID=?", (ID_alvo,))
        resultado = cursor.fetchone()
        if resultado:
            Nome_alvo, CPF_Alvo, Idade_alvo, Sexo_alvo = resultado[0], resultado[1], resultado[2], resultado[3]
            print(f"DADOS PARA EXCLUSÃO: {Nome_alvo} | CPF: {CPF_Alvo}")
            print("-" * 45)
            Confirmar = input("Tem Certeza que quer excluir S/N ").upper()
            if Confirmar == "S":
                cursor.execute("DELETE FROM Clientes WHERE ID=?", (ID_alvo,))
                conn.commit()
                print(f"✅ Cliente Deletado!")
            else:
                print("Operação cancelada")
        else:
            print("ID não encontrado.")
    except sqlite3.Error as erro:
        print("Erro", erro)
    input("Aperte ENTER para continuar...")


def alterar_Clientes(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("=" * 45)
        print("Alterar Clientes")
        print("=" * 45)

        # PROTEÇÃO ID
        while True:
            entrada = input("Insira o ID do cliente: ").strip()
            if entrada.isdigit():
                ID_alvo = int(entrada)
                break
            print("⚠️ Erro: O ID deve ser um número!")

        cursor.execute("SELECT * FROM Clientes WHERE ID=?", (ID_alvo,))
        resultado = cursor.fetchone()
        if resultado:
            print("Dados atuais:", resultado)
            print("-" * 45)
            Novo_Nome = input("Novo nome (Enter p/ manter): ").strip() or resultado[1]

            # PROTEÇÃO NOVA IDADE
            while True:
                Nova_Idade = input("Nova Idade (Enter p/ manter): ").strip() or resultado[4]
                if str(Nova_Idade).isdigit(): break
                print("⚠️ Digite apenas números!")

            Novo_Sexo = input("Novo Sexo (Enter p/ manter): ").strip().upper() or resultado[3]

            confirmar = input("Confirmar alteração S/N? ").upper()
            if confirmar == "S":
                cursor.execute("UPDATE Clientes SET Nome = ?, Sexo = ?, Idade = ? WHERE ID=?",
                               (Novo_Nome, Novo_Sexo, Nova_Idade, ID_alvo))
                conn.commit()
                print("✅ Cliente alterado!")
        else:
            print("ID não encontrado")
    except Exception as erro:
        print("Erro", erro)
    input("Aperte ENTER para continuar...")


def Cadastrar_Veiculos(conn):
    limpar_tela()
    print("=" * 30)
    print("Cadastro de Veículos")
    print("=" * 30)
    try:
        MARCA = input("Informe a Marca: ")
        MODELO = input("Informe a Modelo: ")

        # PROTEÇÃO ANO
        while True:
            ANO = input("Informe o Ano: ").strip()
            if ANO.isdigit(): break
            print("⚠️ Digite apenas números para o ano!")

        PLACA = input("Informe a Placa: ")

        # PROTEÇÃO ID DONO
        while True:
            ID_DONO = input("Informe o ID do comprador: ").strip()
            if ID_DONO.isdigit(): break
            print("⚠️ Digite apenas números para o ID do comprador!")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Veiculos(MARCA,MODELO,ANO,PLACA,ID_DONO) VALUES(?,?,?,?,?)",
                       (MARCA, MODELO, ANO, PLACA, ID_DONO))
        conn.commit()
        print("✅ Veículo cadastrado!")
    except sqlite3.Error as erro:
        print("Erro no Banco de Dados", erro)
    input("Aperte ENTER para continuar...")


def Listar_Veiculos(conn):
    try:
        limpar_tela()
        print("=" * 45)
        print("Lista de Veiculos")
        print("=" * 45)
        df = pd.read_sql_query("SELECT * FROM Veiculos", conn)
        if df.empty:
            print("Lista Vazia")
        else:
            print("=" * 45)
            print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
            print("=" * 60)
        input("Aperte ENTER para voltar ao menu")
    except Exception as erro:
        print("Erro", erro)


def Alterar_Modelos(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("=" * 45)
        print("Alterar Modelo")
        print("=" * 45)

        # PROTEÇÃO ID
        while True:
            ID = input("Informe o ID do Modelo: ").strip()
            if ID.isdigit(): break
            print("⚠️ Digite apenas números!")

        cursor.execute("SELECT * FROM Veiculos WHERE ID=?", (ID,))
        resultado = cursor.fetchone()
        if resultado:
            print("Veículo atual:", resultado)
            print("=" * 45)
            nova_Marca = input("Novo Marca: ").strip() or resultado[1]
            novo_Modelo = input("Novo Modelo: ").strip() or resultado[2]

            # PROTEÇÃO NOVO ANO
            while True:
                ano_Veiculo = input("Novo Ano: ").strip() or resultado[3]
                if str(ano_Veiculo).isdigit(): break
                print("⚠️ Digite apenas números!")

            placa_nova = input("Nova Placa: ").strip() or resultado[4]

            cursor.execute("UPDATE Veiculos SET MARCA=?, MODELO=?, ANO=?, PLACA=? WHERE ID=?",
                           (nova_Marca, novo_Modelo, ano_Veiculo, placa_nova, ID))
            conn.commit()
            print("✅ Veículo alterado com sucesso")
        else:
            print("ID Não encontrada")
    except sqlite3.Error as erro:
        print("Erro", erro)
    input("Aperte ENTER para continuar...")


def Deletar_Modelos(conn):
    try:
        limpar_tela()
        cursor = conn.cursor()
        print("=" * 45)
        print("Deletar Modelo")
        print("=" * 45)

        # PROTEÇÃO ID
        while True:
            ID_Alvo = input("Informe o ID do Modelo: ").strip()
            if ID_Alvo.isdigit(): break
            print("⚠️ Digite apenas números!")

        cursor.execute("SELECT * FROM Veiculos WHERE ID=?", (ID_Alvo,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Dados para exclusão: {resultado[1]} {resultado[2]}")
            Confirmar = input("Confirmar exclusão S/N? ").upper()
            if Confirmar == "S":
                cursor.execute("DELETE FROM Veiculos WHERE ID=?", (ID_Alvo,))
                conn.commit()
                print(f"✅ Veículo deletado!")
            else:
                print("Operação cancelada")
        else:
            print("Veículo não encontrado")
    except sqlite3.Error as erro_sql:
        print("Erro", erro_sql)
    input("Aperte ENTER para voltar...")


# --- MENUS MANTIDOS IGUAIS ---
def Cadastro_clientes_Menu():
    try:
        while True:
            limpar_tela()
            print("=" * 30)
            print("==========Menu Do Sub_Sistema=========")
            print("=" * 30)
            print("[1] Cadastrar Cliente")
            print("[2] Listar clientes")
            print("[3] alterar dados")
            print("[4] Deletar dados")
            print("[0] Sair")
            print("=" * 35)
            opcao = input("Escolha A Opção: ").strip()
            match opcao:
                case "1":
                    cadastra_Clientes(conexao)
                case "2":
                    Listar_Clientes(conexao)
                case "3":
                    alterar_Clientes(conexao)
                case "4":
                    deletar_Clientes(conexao)
                case "0":
                    break
                case _:
                    print("Opção Inválida")
    except Exception as erro:
        print("Erro", erro)


def Cadastro_veiculos_Menu():
    try:
        while True:
            limpar_tela()
            print("=" * 30)
            print("========Menu Do Sub_Sistema=========")
            print("=" * 30)
            print("1: Cadastrar Veículo")
            print("2: Listar Modelos")
            print("3: Alterar Modelo")
            print("4: Deletar Modelo")
            print("0: Sair")
            print("=" * 35)
            opcao = input("Escolha A Opção: ").strip()
            match opcao:
                case "1":
                    Cadastrar_Veiculos(conexao)
                case "2":
                    Listar_Veiculos(conexao)
                case "3":
                    Alterar_Modelos(conexao)
                case "4":
                    Deletar_Modelos(conexao)
                case "0":
                    break
    except Exception as erro:
        print("Erro", erro)


while True:
    print("=" * 35)
    print(f"{'Menu do Sistema':^45}")
    print("=" * 35)
    print("1: Sub-Menu Clientes")
    print("2: Sub-Menu Veiculos")
    print("0: Sair")
    OP = input("Escolha a Opção: ").strip()
    limpar_tela()
    match OP:
        case "1":
            Cadastro_clientes_Menu()
        case "2":
            Cadastro_veiculos_Menu()
        case "0":
            if conexao: conexao.close()
            break
        case _:
            print("Opção Inválida")