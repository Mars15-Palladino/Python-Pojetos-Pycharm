import os
import sqlite3
from math import trunc
from symtable import Class
from unittest import case

import pandas as panda # chamo o panda
import pandas as pd
from tabulate import  tabulate # importo as tabelas bonitas
import sqlite3 as sql #Chamo a ferramenta do Banco de dados

class CLIENTES:
    def __init__(self,ID_C,CPF,NOME,SEXO,IDADE):
        self.ID_C = ID_C
        self.CPF = CPF
        self.NOME = NOME
        self.SEXO = SEXO
        self.IDADE = IDADE
class clientesOperacao:
    def __init__(self,ConexaoAoBanCO):
        self.ConnP = ConexaoAoBanCO
    def inserirCliente(self,ClientesIN):
        """Aqui receba os comandos e os traduzo para o sql"""
        try:
            cursorP = self.ConnP.cursor()
            sql = "INSERT INTO CLIENTES(CPF,NOME,SEXO,IDADE) VALUES (?,?,?,?)"# AS INTERROGAÇÕES DEVEM BATER COM OS PARÂMETROS
            # OS DADOS VIRAM LÁ DEBAIXO
            valoresP = (ClientesIN.CPF,ClientesIN.NOME,ClientesIN.SEXO,ClientesIN.IDADE)
            cursorP.execute(sql, valoresP)#Aqui eu mando os dados para o banco para serem salvos
            self.ConnP.commit()
            print("Cliente adicionado com sucesso")
            return True
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)
    def listarClientes(self,ClientesIN):
        """Aqui recebe os comandos e os traduzo para o sql"""
        try:
            cursorP = self.ConnP.cursor()
            listaClientes = pd.read_sql_query("SELECT * FROM CLIENTES", self.ConnP)
            print(tabulate(listaClientes, headers="keys", tablefmt="fancy_grid", showindex=False))
            return listaClientes
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)
    def alterarClientes(self,ClientesIN):
        """Aqui Procedimento para alteração do cadastro"""
        try:
            cursorP = self.ConnP.cursor()
            cursorP.execute("SELECT * FROM CLIENTES WHERE ID_C = ?", (ClientesIN.ID_C,))
            ClienteAlterar = cursorP.fetchone()  # fetchone, pega apenas a linha referida
            if not ClienteAlterar:
                print("Cliente não encontrado")
                return False
            print(f"Dados Há deletar {ClienteAlterar[1]} | {ClienteAlterar[2]} | {ClienteAlterar[3]} | {ClienteAlterar[4]}")
            confirmar = input("Deseja alterar os clientes? (S/N) ").strip().upper()
            if confirmar == "S":
                    cursorP = self.ConnP.cursor()
                    sql = "UPDATE CLIENTES SET CPF=?,NOME=?,SEXO=?,IDADE=? WHERE ID_C = ?"
                    valoresP = (ClientesIN.CPF,ClientesIN.NOME,ClientesIN.SEXO,ClientesIN.IDADE,ClientesIN.ID_C,)
                    cursorP.execute(sql, valoresP)
                    self.ConnP.commit()
                    print("Cliente alterado com sucesso")
                    print("Aperte enter para continuar ou voltar ao menu")
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)

    def deletarClientes(self,ClientesIN):
        """Aqui Procedimento para deletar os clientes"""
        try:
            #Procurar o cliente pelo ID e depois deletar
            cursorP = self.ConnP.cursor()
            cursorP.execute("SELECT * FROM CLIENTES WHERE ID_C = ?",(ClientesIN.ID_C,))
            ClienteExclusao = cursorP.fetchone()# fetchone, pega apenas a linha referida
            if not ClienteExclusao:
                print("Cliente Não encontrado no sistema")
                print("Aperte enter para continuar ou voltar ao menu")
                return False
            print(f"Alteração de Dados: {ClienteExclusao[1]} | {ClienteExclusao[2]} | {ClienteExclusao[3]} | {ClienteExclusao[4]}")

            confirmar = input("Deseja deletar os clientes? (S/N) ").strip().upper()
            if confirmar == "S":
                sql = "DELETE FROM CLIENTES WHERE ID_C = ?"
                cursorP.execute(sql, (ClientesIN.ID_C,))#lembre se de colocar a vírgula para transformar em Tupla
                self.ConnP.commit()
                if cursorP.rowcount > 0:
                    print("Cliente deletado com sucesso")
                    input("Aperte enter para continuar ou voltar ao menu")
                return True
            else:
                print("Operação Cancelada")
                return False
        except sqlite3.Error as erro:
                print("Erro no banco de dados.",erro)


class VEICULOS:
    def __init__(self,ID_V,MARCA,MODELO,ANO,PLACA,ID_DONO,):
        self.ID_V = ID_V
        self.MARCA = MARCA
        self.MODELO = MODELO
        self.ANO = ANO
        self.PLACA = PLACA
        self.ID_DONO = ID_DONO

class veiculosOperacao:
    def __init__(self, ConexaoAoBanCO):
        self.ConnP = ConexaoAoBanCO
    def inserirVeiculo(self,VeiculosIN):
        """Aqui recebo os comandos e os traduzo para o sql"""
        try:
            cursorP = self.ConnP.cursor()
            sql = "INSERT INTO VEICULOS(MARCA,MODELO,ANO,PLACA,ID_DONO) VALUES (?,?,?,?,?)"# AS INTERROGAÇÕES DEVEM BATER COM OS PARÂMETROS
            #AQUI OS DADOS VIRAM LÁ DE BAIXO
            valoresP = (VeiculosIN.MARCA,VeiculosIN.MODELO,VeiculosIN.ANO,VeiculosIN.PLACA,VeiculosIN.ID_DONO)
            cursorP.execute(sql, valoresP)
            self.ConnP.commit()
            print("Veiculo adicionado com sucesso")
            return True
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)

    def listarVeiculos(self,VeiculosIN):
        """Aqui recebe os comandos e os traduzo para o sql"""
        try:
            cursorP = self.ConnP.cursor()
            listaVeiculos = pd.read_sql_query("SELECT * FROM VEICULOS", self.ConnP)# só cham o comando
            print(tabulate(listaVeiculos,headers="keys", tablefmt="fancy_grid", showindex=False))
            return listaVeiculos
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)

    def alterarVeiculo(self,VeiculosIN):
        try:
            cursorP = self.ConnP.cursor()
            cursorP.execute("SELECT * FROM VEICULOS WHERE ID_V=?",(VeiculosIN.ID_V,))
            veiculoAlterar = cursorP.fetchone()
            if not veiculoAlterar:
                print("Veiculo não encontrado no sistema")
                return False
            print(f"Veiculo Ha ser alterado {veiculoAlterar[0]} | {veiculoAlterar[1]} | {veiculoAlterar[2]} | {veiculoAlterar[3]} | {veiculoAlterar[4]} | {veiculoAlterar[5]}")
            confirmar = input("Alterar Veiculo? (S/N) ").strip().upper()
            if confirmar == "S":
                sql = "UPDATE VEICULOS SET MARCA=?,MODELO=?,ANO=?,PLACA=?, ID_DONO=? WHERE ID_V=?"
                valoresP = (VeiculosIN.MARCA,VeiculosIN.MODELO,VeiculosIN.ANO,VeiculosIN.PLACA,VeiculosIN.ID_DONO,VeiculosIN.ID_V)
                cursorP.execute(sql, valoresP)
                self.ConnP.commit()
                print("Veiculo alterado com sucesso")
                input("Pressione ENTER para continuar")
                return True
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)
    def deletarVeiculo(self,VeiculoIN):
        try:
            cursorP = self.ConnP.cursor()
            cursorP.execute("SELECT * FROM VEICULOS WHERE ID_V=?",(VeiculoIN.ID_V,))
            veiculoDeletar = cursorP.fetchone()
            if not veiculoDeletar:
                print("Veiculo nã encontrado no sistema")
                return False
            print(f"Veiculo ha ser deletado: {veiculoDeletar[0]} | {veiculoDeletar[1]} | {veiculoDeletar[2]} | {veiculoDeletar[3]} | {veiculoDeletar[4]} | {veiculoDeletar[5]}")
            consfirmar = input("Deletar Veiculo? (S/N) ").strip().upper()
            if consfirmar == "S":
                sql = "DELETE FROM VEICULOS WHERE ID_V=?"
                cursorP.execute(sql,(VeiculoIN.ID_V,))
                self.ConnP.commit()
                print("Veiculo deletado com sucesso")
                return True
            else:
                print("Operação Cancelada")
                return False
        except sqlite3.Error as erro:
            print("Erro no banco de dados.",erro)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
def iniciar_Banco_De_Dados():
    try:
        connP = sqlite3.connect('banco_de_dados_Financiamento.db')
        print("..............Conectado Ao Banco de Dados.............", sqlite3.sqlite_version)
        connP.execute("PRAGMA foreign_keys = ON")
        cursorP = connP.cursor()# Libera a conexão com o tunel para trabalhar com o Banco de dados

        cursorP.execute('''CREATE TABLE IF NOT EXISTS CLIENTES(ID_C INTEGER PRIMARY KEY AUTOINCREMENT,  
                        CPF VARCHAR(14) NOT NULL UNIQUE,
                        NOME VARCHAR(40) NOT NULL,
                        SEXO VARCHAR(1) NOT NULL,
                        IDADE INTEGER NOT NULL DEFAULT 0)''')

        """#return connP # para usar nas classes POO, PORÉM DEVE SER ABERTO AO FINAL DA OPERAÇÃO"""

        cursorP.execute('''CREATE TABLE IF NOT EXISTS VEICULOS(ID_V INTEGER PRIMARY KEY AUTOINCREMENT,
                        MARCA VARCHAR(15) NOT NULL,
                        MODELO VARCHAR(45) NOT NULL,
                        PLACA VARCHAR(10) NOT NULL,
                        ANO INTEGER NOT NULL,
                        ID_DONO INTEGER NOT NULL,
                        FOREIGN KEY (ID_DONO) REFERENCES CLIENTES(ID_C))''')
        connP.commit()# passa e carimba a informação
        print("Liberado para Uso")
        return connP
    except sqlite3.Error as erro:
        print("Erro na conexão com banco de dados.",erro)
        return None # Aqui, para o que está fazendo se der erro
limpar_tela()
conexaoAoBanCO = iniciar_Banco_De_Dados()#Aqui abro a conexão para o banco de dados, através da função
if not conexaoAoBanCO:
    print("Erro fatal. Não foi Possível conectar ao banco de dados.")
    input("Pressione ENTER para sair")

def Cadastro_Clientes_Menu():
    limpar_tela()
    operacao = clientesOperacao(conexaoAoBanCO)# faz o código usar a conexão cria aqui em cima
    while True:
        limpar_tela()
        try:
            print("-" * 30)
            print("  SUB-MENU: CLIENTES")
            print("-" * 30)
            print("[1] Inserir Cliente")
            print("[2] Listar Todos")
            print("[3] Alterar Cadastro")
            print("[4] Deletar Registro")
            print("[0] Voltar")
            escolha = input("Escolha a Opcao: ").strip()
            match escolha:
                case "1":
                     novo_Cliente = CLIENTES(None,
                                             input("Insira o CPF do Cliente").strip(),# .strip, não serve para inteiros, apenas para letras
                                             input("Insira o NOME do cliente: ").strip(),
                                             input("Insira o SEXO do cliente: ").strip(),
                                             int(input("Insira a IDADE do cliente: ")))
                     operacao.inserirCliente(novo_Cliente)
                case "2":
                    print("="*45)
                    print("Lista de Clientes Cadastrados")
                    print("="*45)
                    operacao.listarClientes(None)
                    input("Aperte enter para continuar...")
                    print("="*45)
                case "3":
                    id_cliente = int(input("Insira o ID do cliente que deseja fazer alterações: "))
                    #pedindo novos dados para atualizar
                    mudar = CLIENTES(id_cliente,
                                     input("Insira o CPF do cliente: ").strip(),
                                     input("Insira o NOME a alterar: ").strip(),
                                     input("Insira o SEXO do cliente: ").strip(),
                                     int(input("Insira a IDADE do cliente: "))
                                     )
                    print("!AVISO")
                    print("="*45)
                    input("Aperte enter para continuar...")
                    print("="*45)
                    print("Leia com atenção as Mensagens")
                    input("Aperte enter para continuar...")
                    operacao.alterarClientes(mudar)
                case "4":
                    print("="*45)
                    print("Deletar Cliente")
                    print("="*45)
                    id_cliente = int(input("Insira o ID do cliente: "))
                    # pedindo dados para deletar
                    deletar_Alvo = CLIENTES(id_cliente,None,None,None,None)
                    operacao.deletarClientes(deletar_Alvo)
                case "0":
                    limpar_tela()
                    print("="*45)
                    print("Retornando ao Menu Principal")
                    input("Aperte enter para ir ao menu...")
                    break
                case _:
                    print("Apenas opções em Lista")
                    input("Aperte enter para ir ao menu...")
        except Exception as erro:
            print("Erro na lista de Clientes",erro)
            input("Aperte enter para ir ao menu...")
        except ValueError as erro:
            print("Você digitou uam letra onde era esperado Número",erro)
            input("Aperte enter para ir ao menu...")


def Cadastro_Veiculos_Menu():
    limpar_tela()
    # Faz o código usar a conexão global e a classe de operação de veículos
    operacao_v = veiculosOperacao(conexaoAoBanCO)
    # Importante: para cadastrar um veículo, precisamos saber quem são os clientes (donos)
    operacao_c = clientesOperacao(conexaoAoBanCO)

    while True:
        limpar_tela()
        try:
            print("-" * 30)
            print("  SUB-MENU: VEÍCULOS")
            print("-" * 30)
            print("[1] Inserir Veículo")
            print("[2] Listar Todos")
            print("[3] Alterar Cadastro")
            print("[4] Deletar Registro")
            print("[0] Voltar")

            escolha = input("Escolha a Opção: ").strip()

            match escolha:
                case "1":
                    print("--- Lista de Clientes (Donos) ---")
                    operacao_c.listarClientes(None)  # Mostra os clientes para o usuário saber o ID_DONO

                    novo_V = VEICULOS(
                        None,
                        input("Insira a MARCA: ").strip(),
                        input("Insira o MODELO: ").strip(),
                        int(input("Insira o ANO: ")),
                        input("Insira a PLACA: ").strip(),
                        int(input("Insira o ID do DONO (Cliente): "))
                    )
                    operacao_v.inserirVeiculo(novo_V)
                    input("Aperte enter para continuar...")

                case "2":
                    print("=" * 45)
                    print("Lista de Veículos Cadastrados")
                    print("=" * 45)
                    operacao_v.listarVeiculos(None)
                    input("Aperte enter para continuar...")

                case "3":
                    id_v = int(input("Insira o ID do VEÍCULO que deseja alterar: "))
                    mudar_v = VEICULOS(
                        id_v,
                        input("Nova MARCA: ").strip(),
                        input("Novo MODELO: ").strip(),
                        int(input("Novo ANO: ")),
                        input("Nova PLACA: ").strip(),
                        int(input("Novo ID do DONO: "))
                    )
                    print("!AVISO: Verifique os dados antes de confirmar")
                    operacao_v.alterarVeiculo(mudar_v)
                    input("Aperte enter para continuar...")

                case "4":
                    print("=" * 45)
                    print("Deletar Veículo")
                    print("=" * 45)
                    id_v = int(input("Insira o ID do veículo para deletar: "))
                    # VEICULOS precisa de 6 argumentos no __init__
                    deletar_alvo = VEICULOS(id_v, None, None, None, None, None)
                    operacao_v.deletarVeiculo(deletar_alvo)
                    input("Aperte enter para continuar...")

                case "0":
                    print("Retornando ao Menu Principal...")
                    break

                case _:
                    print("Opção inválida!")
                    input("Aperte enter para continuar...")

        except ValueError:
            print("Erro: Você digitou letras onde era esperado um número (Ano ou ID).")
            input("Aperte enter para voltar...")
        except Exception as erro:
            print(f"Erro na operação de Veículos: {erro}")
            input("Aperte enter para voltar...")




while True:
    print("="*55)
    print(f"{'Menu Principal':^55}")
    print("="*55)
    print("[1] SUB-S-Cadastrar Cliente")
    print("[2] SUB-S_Cadastrar Veiculo")
    print("[0] SAIR")
    OP = input("Escolha a Opção:").strip().upper()
    limpar_tela()
    match OP:
        case "1":
            Cadastro_Clientes_Menu()
        case "2":
            Cadastro_Veiculos_Menu()
        case "0":
            if conexaoAoBanCO:
                conexaoAoBanCO.close()
                break
        case _:
            print("Apenas opções listadas")