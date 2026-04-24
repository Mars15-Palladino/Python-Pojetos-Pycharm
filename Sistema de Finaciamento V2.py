import os
import sqlite3
from unittest import case

import pandas as pd
from tabulate import tabulate


# =================================================================
# CLASSES DE ENTIDADE (MODELO)
# =================================================================
class CLIENTES:
    def __init__(self, ID_C, CPF, NOME, SEXO, IDADE):
        self.ID_C = ID_C
        self.CPF = CPF
        self.NOME = NOME
        self.SEXO = SEXO
        self.IDADE = IDADE


class VEICULOS:
    def __init__(self, ID_V, MARCA, MODELO, ANO, PLACA, ID_DONO):
        self.ID_V = ID_V
        self.MARCA = MARCA
        self.MODELO = MODELO
        self.ANO = ANO
        self.PLACA = PLACA
        self.ID_DONO = ID_DONO


# =================================================================
# CLASSES DE OPERAÇÃO (REPOSITÓRIO)
# =================================================================
class clientesOperacao:
    def __init__(self, ConexaoAoBanCO):
        self.ConnP = ConexaoAoBanCO

    def inserirCliente(self, ClientesIN):
        try:
            cursorP = self.ConnP.cursor()
            sql = "INSERT INTO CLIENTES(CPF,NOME,SEXO,IDADE) VALUES (?,?,?,?)"
            valoresP = (ClientesIN.CPF, ClientesIN.NOME, ClientesIN.SEXO, ClientesIN.IDADE)
            cursorP.execute(sql, valoresP)
            self.ConnP.commit()
            print("✅ Cliente adicionado com sucesso")
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def listarClientes(self):
        try:
            listaClientes = pd.read_sql_query("SELECT * FROM CLIENTES", self.ConnP)
            return listaClientes
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def alterarClientes(self, ClientesIN):
        try:
            cursorP = self.ConnP.cursor()
            sql = "UPDATE CLIENTES SET CPF=?, NOME=?, SEXO=?, IDADE=? WHERE ID_C = ?"
            valoresP = (ClientesIN.CPF, ClientesIN.NOME, ClientesIN.SEXO, ClientesIN.IDADE, ClientesIN.ID_C)
            cursorP.execute(sql, valoresP)
            self.ConnP.commit()
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def deletarClientes(self, ID_C):
        try:
            cursorP = self.ConnP.cursor()
            sql = "DELETE FROM CLIENTES WHERE ID_C = ?"
            cursorP.execute(sql, (ID_C,))
            self.ConnP.commit()
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)


class veiculosOperacao:
    def __init__(self, ConexaoAoBanCO):
        self.ConnP = ConexaoAoBanCO

    def inserirVeiculo(self, VeiculosIN):
        try:
            cursorP = self.ConnP.cursor()
            sql = "INSERT INTO VEICULOS(MARCA,MODELO,ANO,PLACA,ID_DONO) VALUES (?,?,?,?,?)"
            valoresP = (VeiculosIN.MARCA, VeiculosIN.MODELO, VeiculosIN.ANO, VeiculosIN.PLACA, VeiculosIN.ID_DONO)
            cursorP.execute(sql, valoresP)
            self.ConnP.commit()
            print("✅ Veículo adicionado com sucesso")
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def listarVeiculos(self):
        try:
            listaVeiculos = pd.read_sql_query("SELECT * FROM VEICULOS", self.ConnP)
            return listaVeiculos
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def alterarVeiculo(self, VeiculosIN):
        try:
            cursorP = self.ConnP.cursor()
            sql = "UPDATE VEICULOS SET MARCA=?, MODELO=?, ANO=?, PLACA=?, ID_DONO=? WHERE ID_V=?"
            valoresP = (VeiculosIN.MARCA, VeiculosIN.MODELO, VeiculosIN.ANO, VeiculosIN.PLACA, VeiculosIN.ID_DONO,
                        VeiculosIN.ID_V)
            cursorP.execute(sql, valoresP)
            self.ConnP.commit()
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)

    def deletarVeiculo(self, ID_V):
        try:
            cursorP = self.ConnP.cursor()
            sql = "DELETE FROM VEICULOS WHERE ID_V=?"
            cursorP.execute(sql, (ID_V,))
            self.ConnP.commit()
            return True
        except sqlite3.Error as erro:
            print("⚠️ Erro no banco de dados.", erro)


# =================================================================
# FUNÇÕES DE INTERAÇÃO (MENUS)
# =================================================================

def cadastra_Clientes(conn):
    print("=" * 45)
    print("Cadastro de Clientes")
    print("=" * 45)
    Nome = input("Insira o nome do cliente: ").strip()
    CPF = input("Insira o CPF do cliente: ").strip()
    Sexo = input("Insira o sexo do cliente M/F: ").strip().upper()
    while True:
        Idade = input("Insira a Idade do cliente: ").strip()
        if Idade.isdigit(): break
        print("⚠️ Erro: Digite apenas números!")

    novo_cliente = CLIENTES(None, CPF, Nome, Sexo, int(Idade))
    operacao = clientesOperacao(conn)
    operacao.inserirCliente(novo_cliente)
    input("\nAperte ENTER para voltar ao menu")

def Listar_Clientes(conn):
    limpar_tela()
    print("=" * 45)
    print("Lista de Clientes")
    print("=" * 45)
    operacao = clientesOperacao(conn)
    df = operacao.listarClientes()
    if df is None or df.empty:
        print("Lista Vazia")
    else:
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        input("\nAperte ENTER para voltar ao menu")


def deletar_Clientes(conn):
    limpar_tela()
    print("=" * 45)
    print("Deletar Clientes")
    print("=" * 45)
    while True:
        entrada = input("Insira o ID do cliente: ").strip()
        if entrada.isdigit():
            ID_alvo = int(entrada)
            break
        print("⚠️ Erro: O ID deve ser um número!")

    operacao = clientesOperacao(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENTES WHERE ID_C=?", (ID_alvo,))
    resultado = cursor.fetchone()

    if resultado:
        print(f"DADOS: {resultado[2]} | CPF: {resultado[1]}")
        confirmar = input("Confirmar exclusão S/N? ").upper()
        if confirmar == "S":
            operacao.deletarClientes(ID_alvo)
            print("✅ Cliente Deletado!")
    else:
        print("❌ ID não encontrado.")
        input("Aperte ENTER para continuar...")


def alterar_Clientes(conn):
    limpar_tela()
    print("=" * 45)
    print("Alterar Clientes")
    print("=" * 45)
    while True:
        entrada = input("Insira o ID do cliente: ").strip()
        if entrada.isdigit():
            ID_alvo = int(entrada)
            break
        print("⚠️ Erro: O ID deve ser um número!")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENTES WHERE ID_C=?", (ID_alvo,))
    res = cursor.fetchone()
    if res:
        print("Dados atuais:", res)
        novo_nome = input("Novo nome (Enter p/ manter): ").strip() or res[2]
        novo_cpf = input("Novo CPF (Enter p/ manter): ").strip() or res[1]
        nova_idade = input("Nova Idade (Enter p/ manter): ").strip() or res[4]
        novo_sexo = input("Novo Sexo (Enter p/ manter): ").strip().upper() or res[3]

        cliente_editado = CLIENTES(ID_alvo, novo_cpf, novo_nome, novo_sexo, int(nova_idade))
        operacao = clientesOperacao(conn)
        if operacao.alterarClientes(cliente_editado):
            print("✅ Cliente alterado!")
    else:
        print("❌ ID não encontrado")
        input("Aperte ENTER para continuar...")


def Cadastrar_Veiculos(conn):
    limpar_tela()
    print("=" * 30)
    print("Cadastro de Veículos")
    print("=" * 30)
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    while True:
        ano = input("Ano: ").strip()
        if ano.isdigit(): break
    placa = input("Placa: ").strip()
    while True:
        id_dono = input("ID do Comprador: ").strip()
        if id_dono.isdigit(): break

    novo_carro = VEICULOS(None, marca, modelo, int(ano), placa, int(id_dono))
    estoque = veiculosOperacao(conn)
    estoque.inserirVeiculo(novo_carro)
    input("Aperte ENTER para continuar...")


def Listar_Veiculos(conn):
    limpar_tela()
    print("=" * 45)
    print("Lista de Veículos")
    print("=" * 45)
    estoque = veiculosOperacao(conn)
    df = estoque.listarVeiculos()
    if df is None or df.empty:
        print("Lista Vazia")
    else:
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        input("\nAperte ENTER para voltar")


def Alterar_Modelos(conn):
    limpar_tela()
    print("=" * 45)
    print("Alterar Modelo")
    print("=" * 45)
    id_v = input("Informe o ID do Veículo: ").strip()
    if not id_v.isdigit(): return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VEICULOS WHERE ID_V=?", (id_v,))
    res = cursor.fetchone()
    if res:
        print("Dados atuais:", res)
        m = input("Nova Marca: ").strip() or res[1]
        mod = input("Novo Modelo: ").strip() or res[2]
        a = input("Novo Ano: ").strip() or res[4]
        p = input("Nova Placa: ").strip() or res[3]
        d = input("Novo ID Dono: ").strip() or res[5]

        editado = VEICULOS(id_v, m, mod, int(a), p, int(d))
        operacao = veiculosOperacao(conn)
        operacao.alterarVeiculo(editado)
        print("✅ Veículo alterado!")
    else:
        print("❌ Veículo não encontrado")
        input("Aperte ENTER para continuar...")


def Deletar_Modelos(conn):
    try:
        limpar_tela()
        print("=" * 45)
        print("Deletar Modelo")
        print("=" * 45)
        id_v = input("ID do Veículo para deletar: ").strip()
        if not id_v.isdigit(): return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VEICULOS WHERE ID_V=?", (id_v,))
        res = cursor.fetchone()
        print(f"Veículo atual:, {res[1]} | {res[2]} | {res[3]} | {res[4]} | {res[5]}")
        confirmar = input("Deseja excluir? S/N...").strip().upper()
        if confirmar == "S":
            operacao = veiculosOperacao(conn)
            if operacao.deletarVeiculo(int(id_v)):
                print("✅ Veículo removido!")
            else:
                print("Nenhum veículo pertencente a essa ID_V")
        else:
            print("Operação cancelada!")
            input("Aperte ENTER para continuar...")
    except Exception as e:
        print("Ocorreu um erro",e)
        input("Aperte ENTER para continuar...")

# =================================================================
# SISTEMA PRINCIPAL
# =================================================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def iniciar_Banco_De_Dados():
    try:
        connP = sqlite3.connect('banco_de_dados_Financiamento.db')
        connP.execute("PRAGMA foreign_keys = OFF")
        cursorP = connP.cursor()
        cursorP.execute('''CREATE TABLE IF NOT EXISTS CLIENTES
        (
            ID_C
            INTEGER
            PRIMARY
            KEY
            AUTOINCREMENT,
            CPF
            VARCHAR
                           (
            14
                           ) NOT NULL UNIQUE,
            NOME VARCHAR
                           (
                               40
                           ) NOT NULL,
            SEXO VARCHAR
                           (
                               1
                           ) NOT NULL,
            IDADE INTEGER NOT NULL DEFAULT 0)''')
        cursorP.execute('''CREATE TABLE IF NOT EXISTS VEICULOS
        (
            ID_V
            INTEGER
            PRIMARY
            KEY
            AUTOINCREMENT,
            MARCA
            VARCHAR
                           (
            15
                           ) NOT NULL,
            MODELO VARCHAR
                           (
                               45
                           ) NOT NULL,
            PLACA VARCHAR
                           (
                               10
                           ) NOT NULL,
            ANO INTEGER NOT NULL,
            ID_DONO INTEGER NOT NULL,
            FOREIGN KEY
                           (
                               ID_DONO
                           ) REFERENCES CLIENTES
                           (
                               ID_C
                           ))''')
        connP.commit()
        return connP
    except sqlite3.Error as erro:
        print("Erro na conexão.", erro)
        return None


def Cadastro_clientes_Menu():
    while True:
        limpar_tela()
        print("========================= Menu Clientes ===========================")
        print("[1] Cadastrar | [2] Listar | [3] Alterar | [4] Deletar | [0] Sair")
        print("===================================================================")
        op = input("Escolha: ").strip()
        match op:
            case "1":
                cadastra_Clientes(conexaoAoBanCO)
            case "2":
                Listar_Clientes(conexaoAoBanCO)
            case "3":
                alterar_Clientes(conexaoAoBanCO)
            case"4":
                deletar_Clientes(conexaoAoBanCO)
            case"0":
                break


def Cadastro_veiculos_Menu():
    while True:
        limpar_tela()
        print("======================== Menu Veículos ===========================")
        print("[1] Cadastrar | [2] Listar | [3] Alterar | [4] Deletar | [0] Sair")
        print("===================================================================")
        op = input("Escolha: ").strip()
        match op:
          case "1":
            Cadastrar_Veiculos(conexaoAoBanCO)
          case "2":
            Listar_Veiculos(conexaoAoBanCO)
          case "3":
            Alterar_Modelos(conexaoAoBanCO)
          case "4":
            Deletar_Modelos(conexaoAoBanCO)
          case "0":
            break


# EXECUÇÃO
conexaoAoBanCO = iniciar_Banco_De_Dados()
if conexaoAoBanCO:
    while True:
        limpar_tela()
        print("=" * 35)
        print(f"{'SISTEMA DE FINANCIAMENTO':^35}")
        print("=" * 35)
        print("1: Sub-Menu Clientes")
        print("2: Sub-Menu Veiculos")
        print("0: Sair")
        OP = input("Escolha a Opção: ").strip()
        if OP == "1":
            Cadastro_clientes_Menu()
        elif OP == "2":
            Cadastro_veiculos_Menu()
        elif OP == "0":
            conexaoAoBanCO.close()
            break