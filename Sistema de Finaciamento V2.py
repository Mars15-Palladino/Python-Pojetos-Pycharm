import os
import sqlite3
from datetime import date

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
    def __init__(self, ID_V, MARCA, MODELO, ANO, PLACA, ID_DONO = None):
        self.ID_V = ID_V
        self.MARCA = MARCA
        self.MODELO = MODELO
        self.ANO = ANO
        self.PLACA = PLACA
        self.ID_DONO = ID_DONO

class FINANCIAMENTO:
    def __init__(self,ID_F,ID_C,ID_V,DATA_COMPRA_INICIO,VALOR,QTD_PARCELAS,):
        self.ID_F = ID_F
        self.ID_C = ID_C
        self.ID_V = ID_V
        self.DATA_COMPRA_INICIO = DATA_COMPRA_INICIO
        self.VALOR = VALOR
        self.QTD_PARCELAS = QTD_PARCELAS

# =================================================================
# CLASSES Das OPERAÇÕES (REPOSITÓRIO)
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
class FinanceiraOperacao:
    def __init__(self, ConexaoAoBanCO):
        self.connP = ConexaoAoBanCO# self organiza a conexão

    def Financiamento_OP_Venda(self, Nova_Venda):

            Nome_Cliente = Nova_Venda.ID_C
            modelo_Veiculo = Nova_Venda.ID_V

            cursorP = self.connP.cursor()
            cursorP.execute("SELECT ID_C,NOME,CPF FROM CLIENTES WHERE NOME LIKE ?", (f"%{Nome_Cliente}%",))
            resultado_Cliente = cursorP.fetchone()

            if not resultado_Cliente:
                print("Cliente Não encontrado no Sistema")
                return
            else:
                print(f"Cliente encontrado,{resultado_Cliente[0]}")
                print(f"Nome do Cliente,{resultado_Cliente[1]}")
                print(f"CPF encontrado,{resultado_Cliente[2]}")
                confirmarC = input("Cliente Correto... (S/N)").strip().upper()
                if confirmarC == "S":
                    print("Operação Concluída!")
                else:
                    print("Operacão Cancelada!")
                input("Aperte ENTER para continuar...")

            cursorP.execute("SELECT ID_V,MODELO,PLACA FROM VEICULOS WHERE MODELO LIKE ?", (f"%{modelo_Veiculo}%",))
            resultado_Veiculo = cursorP.fetchone()

            if not resultado_Veiculo:
                print("Veículo Não encontrado")
                return
            else:
                print(f"Veículo encontrado,{resultado_Veiculo[0]}")
                print(f"Modelo,{resultado_Veiculo[1]}")
                print(f"PLACA encontrado,{resultado_Veiculo[2]}")
                confirmarV = input("Veiculo Correto.....(S/N)").strip().upper()
                if confirmarV == "S":
                    print("Operação Concluída!")
                else:
                    print("Operação Cancelada")
                input("Aperte ENTER para continuar...")
                # Aqui eu uso apenas o que vou usar para as chaves estrangeiras
                ID_cliente_Final = resultado_Cliente[0]
                CPF_cliente_Final = resultado_Cliente[2]
                Nome_cliente_Final = resultado_Cliente[1]

                ID_veiculo_Final = resultado_Veiculo[0]
                Modelo_Veiculo_Final = resultado_Veiculo[1]
                PLACA_Veiculo_Final = resultado_Veiculo[2]
                print("=" * 45)
                print(f"Prosseguindo para valores da Compra do Cliente:{CPF_cliente_Final} | {Nome_cliente_Final}")
                print(f"Veículo escolhido: {Modelo_Veiculo_Final} de | (Placa:{PLACA_Veiculo_Final})")
                print("=" * 45)
                print(f"{'Operação Financeira':^24}")
                print("=" * 45)
                print("1.Pagamento a Vista")
                print("2.Pagamento Parcelado")
                escolha = input("Escolha a Forma de Pagamento")
                Data_Venda = date.today().strftime("%d/%m/%Y")
                ValorFinal = None
                QTD_PARCELAS = None
                ValorFinal_Banco = None
                while True:
                    try:
                        match escolha:
                            case "1":
                                print("Pagamento a Vista")
                                ValorVeiculo = input("Informe o Valor do Veículo: ").strip().replace(",", ".")
                                Valor_Veiculo_Total = float(
                                    ValorVeiculo)  # Em Python, raise significa "lançar" ou "disparar".
                                if Valor_Veiculo_Total <= 0: raise ValueError
                                # quando você escreve isso, você está forçando o programa a gerar um erro propositalmente.
                                # A Lógica: Um carro não pode custar $R$ 0,00$ nem um valor negativo (como $-R$ 5.000,00$).
                                # O Problema: O Python aceita o número -5000 em uma variável do tipo float sem reclamar.
                                # A Solução: Você cria uma regra personalizada. Se o valor for menor ou igual a zero, você "lança" o erro ValueError.
                                print("Desconto de 20%, Aplicacdo para pagamento a Vista")
                                ValorFinal = Valor_Veiculo_Total - (Valor_Veiculo_Total * 0.20)
                                print(f"Compra Aprovada: Valor Final = R$ {ValorFinal:,.2f}")
                                QTD_PARCELAS = 1
                                ValorFinal_Banco = ValorFinal
                                break
                            case "2":
                                print("Pagamento Parcelado")
                                ValorVeiculo = input("Informe o Valor do Veículo: ").strip().replace(",", ".")
                                Valor_Veiculo_Total = float(ValorVeiculo)
                                if Valor_Veiculo_Total <= 0: raise ValueError
                                while True:
                                    try:
                                        QTD_PARCELAS = int(input("Informe em quantas vezes: "))
                                        # if not QTD_PARCELAS.isdigit(): Não funciona para inteiros, apenas para strings, texto
                                        # return
                                        if QTD_PARCELAS <= 0: raise ValueError
                                        break
                                    except ValueError as e:
                                        print("Insira um Valor Váilido")

                                print("Sem desconto Aplicado. Ocorrência de juros de no Máximo até 10,0% de")
                                Taxa_Informada = input("Informe a Taxa dos Juros entre 1,1 a 10,0").strip().replace(",",
                                                                                                                    ".")  # .05 # 5% ao mês
                                Taxa_Juros = float(Taxa_Informada) / 100
                                print("=" * 45)
                                ValorFinal = Valor_Veiculo_Total
                                # Valor_Parcela = Valor_Veiculo_Total/QTD_PARCELAS #Mudança para incluir cálculo de juros abaixo
                                ValorFinal_Juros = Valor_Veiculo_Total * (1 + (Taxa_Juros * QTD_PARCELAS))
                                ValorParcela = ValorFinal_Juros / QTD_PARCELAS
                                print("=" * 45)
                                print("Informações Da Compra")
                                print('-' * 45)
                                print(f"Taxa de Juros: {Taxa_Juros * 100}% ao Mês")
                                print(f"Compra Aprovada: {ValorFinal_Juros:,.2f}")
                                print(f"Parcelamento Aprovado em {QTD_PARCELAS} vezes de R$ {ValorParcela:,.2f} Reais ")
                                print("=" * 45)
                                print(f"Total dos juros: R$ {ValorFinal_Juros - Valor_Veiculo_Total:,.2f}")
                                confirmar = input("Deseja continuar?(S/N)").strip().upper()
                                if confirmar == "S":
                                    print("Operação Concluída")
                                    ValorFinal_Banco = ValorFinal_Juros
                                    break
                                else:
                                    print("Operação Cancelada")
                                    return

                    except ValueError as e:
                        print("Valor invalido: O valor do Veículo e das Parcelas deve ser maior que zero", e)
                        continue

            if ValorFinal is not None:
                try:
                    sql = "INSERT INTO FINANCIAMENTO(ID_C,ID_V,DATA_COMPRA_INICIO,VALOR,QTD_PARCELAS) VALUES (?,?,?,?,?)"
                    cursorP.execute(sql,
                                    (ID_cliente_Final, ID_veiculo_Final, Data_Venda, ValorFinal_Banco, QTD_PARCELAS))
                    self.connP.commit()
                    print("Registro da operação salvo com sucesso!")
                except sqlite3.Error as e:
                    print("Erro no Banco de dados", e)
    def Relatorio_Vendas(self):
        limpar_tela()
        print("=" * 45)
        print("Relatório de Vendas E FIANCIAMENTO")
        print("=" * 45)
        Relatorio_Vendas = pd.read_sql_query("SELECT "
                                      "F.ID_F AS 'ID_F'," # USO DE APELIDOS LIBERADOS INIAL DAS CLASSES PRINCIPAIS
                                      "C.NOME AS 'CLIENTE', "
                                      "V.MODELO AS 'VEICULO', "
                                      "F.DATA_COMPRA_INICIO AS 'Data da Compra', "
                                      "F.VALOR AS 'Valor', "
                                      "F.QTD_PARCELAS AS 'Parcelas'  "
                                      "FROM FINANCIAMENTO F "
                                      "JOIN CLIENTES C ON F.ID_C = C.ID_C "
                                      "JOIN VEICULOS V ON F.ID_V = V.ID_V ", self.connP)
        return Relatorio_Vendas

        #Usando o Join, ele mostra o nome que estão nas outras tabelas no lugar dos números

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

    novo_carro = VEICULOS(None, marca, modelo, int(ano), placa, None)# lembrar de passar como pacote, mas também posso passar as variáveis direto
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
# ================================================================
#                  Operação Financiamento menus
#=================================================================
def Iniciar_Venda_Operacao(conn):
    limpar_tela()
    print("=" * 45)
    print("Financiamento de Compra")
    print("=" * 45)
    Nome_Cliente_Envio = input("Informe o nome do cliente: ").strip()
    modelo_Veiculo_Envio = input("Informe o modelo do Veículo: ").strip()

    Nova_Venda = FINANCIAMENTO(None,Nome_Cliente_Envio, modelo_Veiculo_Envio,None,None,None)
    operador = FinanceiraOperacao(conn)
    operador.Financiamento_OP_Venda(Nova_Venda)
    input("Aperte ENTER para continuar...")
def Listar_Vendas(conn):
    try:

        relatorio = FinanceiraOperacao(conn)# aqui eu criei meu próprio método, é ele que devo chamar a baixo
        df = relatorio.Relatorio_Vendas()
        if df is None or df.empty:
            print("Nenhum relatorio encontrado")
        else:
            print("Relatorio financiamento de Compra")
            print("=" * 45)
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
            print("="*45)
            input("Aperte ENTER para continuar...")
    except sqlite3.Error as e:
                print("Ocorreu um erro no Banco de Dados",e)

# =================================================================
#                      SISTEMA PRINCIPAL
# =================================================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def iniciar_Banco_De_Dados():
    try:
        connP = sqlite3.connect('banco_de_dados_Financiamento.db')
        connP.execute("PRAGMA foreign_keys = ON")
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
            ID_DONO INTEGER,
            FOREIGN KEY
                           (
                               ID_DONO
                           ) REFERENCES CLIENTES
                           (
                               ID_C
                           ))''')
        cursorP.execute('''CREATE TABLE IF NOT EXISTS FINANCIAMENTO(
                        ID_F INTEGER PRIMARY KEY AUTOINCREMENT,
                        ID_C INTEGER NOT NULL,
                        ID_V INTEGER NOT NULL, 
                        DATA_COMPRA_INICIO VARCHAR(15) NOT NULL,
                        VALOR DECIMAL(10,2) NOT NULL, --10 digitos no total, 2 Após Vírgula-- 
                        QTD_PARCELAS INTEGER NOT NULL,
                        FOREIGN KEY (ID_C) REFERENCES CLIENTES
                        FOREIGN KEY (ID_V) REFERENCES VEICULOS) ''')
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
            case _:
                print("Apenas Opções Listadas")
                input("Pressione ENTER para sair")


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
          case _:
              print("Apenas opções Listadas")
              input("Pressione ENTER para sair")
def Compra_Financiamento_Menu():
    while True:
        limpar_tela()
        print("=========================Menu Compra e Vendas============================")
        print("               [1] Compra | [2] relatório de Compras | [0] Sair"          )
        print("========================================================================")
        op = input("Escolha: ").strip()
        match op:
            case "1":
                Iniciar_Venda_Operacao(conexaoAoBanCO)
            case "2":
                Listar_Vendas(conexaoAoBanCO)
            case "0":
                break
            case _:
                print("Apenas opões Listadas")
                input("Pressione ENTER para Retornar ao menu")


conexaoAoBanCO = iniciar_Banco_De_Dados()
if conexaoAoBanCO:
    while True:
        limpar_tela()
        print("=" * 35)
        print(f"{'SISTEMA DE FINANCIAMENTO':^35}")
        print("=" * 35)
        print("1: Sub-Menu Clientes")
        print("2: Sub-Menu Veiculos")
        print("3: Compra")
        print("0: Sair")
        OP = input("Escolha a Opção: ").strip()
        if OP == "1":
            Cadastro_clientes_Menu()
        elif OP == "2":
            Cadastro_veiculos_Menu()
        elif OP == "3":
            Compra_Financiamento_Menu()
        elif OP == "0":
            conexaoAoBanCO.close()
            break