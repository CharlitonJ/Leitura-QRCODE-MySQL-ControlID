import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import datetime
import tkinter as tk
import requests
import configparser

# Criando a janela
janela = Tk()
janela.title("Minerva 2.0")
janela.geometry("300x250")
janela.configure(background="Black")
janela.resizable(width=FALSE, height=FALSE)
# ===============widgets====================
mainframe = Frame(janela, width=512, height=600, bg="Black", relief="raise")

# Variável global para controlar o status do processo
processo_em_execucao = False
session = None  # Variável global para armazenar a sessão após o login

# Função que lê as configurações definidas no Config.ini


def Ler_config():
    global ip_equip
    global login_equip
    global pass_equip
    global ip_serv
    global login_serv
    global pass_serv
    global database
    global port

    # Carregar o arquivo de configuração
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Acessar os dados equipamento
    ip_equip = config["Equipamento"]["Ip_Equip"]
    login_equip = config["Equipamento"]["Login_Equip"]
    pass_equip = config["Equipamento"]["Pass_Equip"]

    # Acessar os dados servidor DB
    ip_serv = config["Servidor"]["ip_Serv"]
    port = config["Servidor"]["port"]
    database = config["Servidor"]["database"]
    login_serv = config["Servidor"]["login_Serv"]
    pass_serv = config["Servidor"]["pass_Serv"]

    # Exibindo dados para controle de erros
    print("Dados do Equipamento:")
    print(f"IP: {ip_equip}, Login: {login_equip}, Senha: {pass_equip}")

    print("\nDados do Servidor:")
    print(f"IP: {ip_serv}, Login: {login_serv}, Senha: {pass_serv}")

# Função para realizar a limpeza


def processar_entrada(*args):
    valor_entrada = var_nf.get()
    print(valor_entrada)
    valor_limpo = valor_entrada.strip()
    print(valor_limpo)
    # Verifica se há algum valor na entrada e o processo não está em execução
    if valor_entrada and not processo_em_execucao:
        print(f"Entrada recebida: {valor_limpo}")
        iniciar_processo()  # Inicia o processo automático assim que a entrada for recebida


# Função para fazer login
def login():
    global session
    login_data = {
        f"login": "{login_equip}",
        "password": "{pass_equip}"
    }

    try:
        # URL do endpoint de login no equipamento (sem a porta 5000)
        url_login = f"http://{ip_equip}/login.fcgi"
        response = requests.post(url_login, json=login_data)

        # Se o login for bem-sucedido
        if response.status_code == 200:
            # Extrai o token ou sessão do retorno
            data = response.json()
            session = data.get('session')

            if session:
                print("Login bem-sucedido! Sessão:", session)
            else:
                print("Falha no login: Sessão não retornada.")
        else:
            print("Erro no login:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Erro ao tentar fazer login:", e)

# Função que realiza o processo automático


def processo_automatico():
    global processo_em_execucao
    valor_entrada = var_nf.get()
    valor_limpo = valor_entrada.strip()

    # Criação de uma nova conexão com o banco de dados para a thread
    try:
        conn = mysql.connector.connect(
            host=ip_serv,
            port=port,
            user=login_serv,
            password=pass_serv,
            database=database
        )
        cursor = conn.cursor()

        if conn.is_connected():
            print("Conexão bem-sucedida ao banco de dados remoto!")

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

    while processo_em_execucao:
        # Obtendo a data atual
        data_hoje = datetime.date.today()
        data_hoje_str = data_hoje.strftime('%Y-%m-%d')

        # Executar a consulta com a data como parâmetro
        cursor.execute(""" 
        SELECT * FROM nfcontrole WHERE dhEmi = %s;
        """, (data_hoje_str,))

        # Pega todos os resultados
        resultados = cursor.fetchall()

        # Exibe os resultados
        for linha in resultados:
            # Verifica se o NumNF está presente em algum valor da linha
            # Converte todos os valores para string antes de comparar
            if valor_limpo in [str(valor) for valor in linha]:
                login()

                url = f"http://{ip_equip}/execute_actions.fcgi?session={session}"
                payload = {
                    "actions": [
                        {"action": "sec_box", "parameters": "id=65793, reason=3"}
                    ]
                }
                headers = {
                    "Content-Type": "application/json",
                }

                try:
                    response = requests.post(
                        url, json=payload, headers=headers)

                    if response.status_code == 200:
                        print("Ação executada com sucesso!")
                    else:
                        print(f"Erro ao chamar a API: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao conectar com a API: {e}")

        var_nf.set("")  # Limpa a entrada após o acionamento
        processo_em_execucao = False

    # Fechando a conexão ao banco de dados após a execução da thread
    if conn and conn.is_connected():
        conn.close()
        print("Conexão encerrada com sucesso.")

# Função para iniciar o processo automático


def iniciar_processo():
    global processo_em_execucao
    if not processo_em_execucao:
        processo_em_execucao = True
        thread = threading.Thread(target=processo_automatico)
        thread.start()

# Função para parar o processo automático


def parar_processo():
    global processo_em_execucao
    if processo_em_execucao:
        processo_em_execucao = False
        messagebox.showinfo("Informação", "Processo parado!")

# Função chamada quando uma entrada de número de nota fiscal for detectada


def on_enter():
    processar_entrada()

# Função da Tela Inicial


def TelaInicial():
    mainframe.pack(side="top")

    # Criação de label e entrada de texto para número de nota fiscal (ou outra entrada)
    label_nf = Label(mainframe, text="Número da NF:", font=(
        "Century Gothic", 14), bg="Black", fg="White")
    label_nf.place(x=35, y=50)

    global var_nf
    # Criando uma StringVar para monitorar as mudanças no campo de entrada
    var_nf = StringVar()

    # Associando a StringVar ao Entry
    entry_nf = tk.Entry(mainframe, width=30, textvariable=var_nf)
    entry_nf.place(x=35, y=80)
    entry_nf.bind("<Return>", on_enter)

    # Criação de botões para parar o processo
    PararButton = ttk.Button(
        mainframe, text="Parar Processo", width=30, command=parar_processo)
    PararButton.place(x=35, y=150)


# Leitura do arquivo config
Ler_config()
# Abertura da tela inicial
TelaInicial()

# Rodando a interface gráfica
janela.mainloop()
