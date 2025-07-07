import sqlite3
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import datetime
import tkinter as tk

# Criando a janela
janela = Tk()
janela.title("Gestok - Controle de Processo Automático")
janela.geometry("300x250")
janela.configure(background="#94438e")
janela.resizable(width=FALSE, height=FALSE)
janela.iconbitmap(default="Tela Login/icons/ICONE.ico")

# ===============widgets====================
leftframe = Frame(janela, width=512, height=600, bg="Black", relief="raise")
rightframe = Frame(janela, width=512, height=600, bg="Black", relief="raise")

# Variável global para controlar o status do processo
processo_em_execucao = False


def processar_entrada(*args):
    valor_entrada = var_nf.get()
    print(valor_entrada)
    valor_limpo = valor_entrada.strip()
    print(valor_limpo)
    # print(valor_entrada)
    # Verifica se há algum valor na entrada e o processo não está em execução
    if valor_entrada and not processo_em_execucao:
        print(f"Entrada recebida: {valor_limpo}")
        iniciar_processo()  # Inicia o processo automático assim que a entrada for recebida

# Função que realiza o processo automático


def processo_automatico():
    global processo_em_execucao
    valor_entrada = var_nf.get()
    valor_limpo = valor_entrada.strip()
    # Criação de uma nova conexão com o banco de dados para a thread
    # Substitua pelo caminho correto do seu banco de dados
    conn = sqlite3.connect('Geral.db')
    cursor = conn.cursor()

    while processo_em_execucao:
        # Obtendo a data atual
        data_hoje = datetime.date.today()
        data_hoje_str = data_hoje.strftime('%d/%m/%Y')

        # Executar a consulta com a data como parâmetro
        NumNF2 = cursor.execute("""
            SELECT * FROM NFcontrole
            WHERE dhEmi = ?
        """, (data_hoje_str,))

        # Pega todos os resultados
        resultados = NumNF2.fetchall()
        # print(resultados)
        # Exibe os resultados
        for linha in resultados:
            # print(linha)
            # Verifica se o NumNF está presente em algum valor da linha (tupla)
            # Converte todos os valores para string antes de comparar
            if valor_limpo in [str(valor) for valor in linha]:
                print("Deu Certo!!")

        if resultados:
            print(f"Resultados encontrados para a data {
                  data_hoje_str}: {resultados}")

        # Atraso para evitar sobrecarga
        var_nf.set("")  # Limpa a entrada após o acionamento
        processo_em_execucao = False

        # print("chama API")

    # Fechando a conexão ao banco de dados após a execução da thread
    conn.close()

# Função para iniciar o processo automático


def iniciar_processo():
    global processo_em_execucao
    if not processo_em_execucao:
        processo_em_execucao = True
        thread = threading.Thread(target=processo_automatico)
        thread.start()
        # messagebox.showinfo("Informação", "Processo iniciado automaticamente!")

# Função para parar o processo automático


def parar_processo():
    global processo_em_execucao
    if processo_em_execucao:
        processo_em_execucao = False
        messagebox.showinfo("Informação", "Processo parado!")

# Função chamada quando uma entrada de número de nota fiscal (ou qualquer dado) for detectada


def on_enter(event):
    processar_entrada()


# Função da Tela Inicial


def TelaInicial():
    leftframe.pack(side=LEFT)
    rightframe.pack(side=RIGHT)

    # Criação de label e entrada de texto para número de nota fiscal (ou outra entrada)
    label_nf = Label(leftframe, text="Número da NF:", font=(
        "Century Gothic", 14), bg="Black", fg="White")
    label_nf.place(x=35, y=50)

    global var_nf
    # Criando uma StringVar para monitorar as mudanças no campo de entrada
    var_nf = StringVar()

    # Associando a StringVar ao Entry
    entry_nf = tk.Entry(leftframe, width=30, textvariable=var_nf)
    entry_nf.place(x=35, y=80)
    entry_nf.bind("<Return>", on_enter)

    # Monitorando a entrada em tempo real (sempre que houver uma mudança, o processo será iniciado)
    # Usando trace para detectar mudanças na StringVar
    # var_nf.trace("w", processar_entrada)

    # Criação de botões para parar o processo
    # IniciarButton = ttk.Button(
    #    leftframe, text="Iniciar Processo", width=30, command=processar_entrada)
    # IniciarButton.place(x=35, y=130)
    PararButton = ttk.Button(
        leftframe, text="Parar Processo", width=30, command=parar_processo)
    PararButton.place(x=35, y=150)


# Abertura da tela inicial
TelaInicial()

# Rodando a interface gráfica
janela.mainloop()
