# Leitura-QRCODE-MySQL-ControlID

Esta aplicação tem como objetivo controlar a saída de veículos e pessoas por meio da leitura de códigos de barras ou QR Codes. Inicialmente, foi desenvolvida para validar chaves de acesso de notas fiscais, integrando-se com equipamentos da Control ID e um banco de dados MySQL.

## Tecnologias Utilizadas

- Python 3.8 ou superior  
- APIs da Control ID  
- MySQL (ou outro banco compatível)  
- Leitor de Código de Barras/QR Code (modo teclado)

## Pré-requisitos

Antes de executar a aplicação, certifique-se de possuir:

- Python 3.8 ou superior instalado  
- Leitor de código de barras ou QR Code conectado à máquina (modo teclado)  
- Acesso ao equipamento Control ID  
- Acesso à API Control ID  
- Acesso ao banco de dados com os dados para validação  
- Máquina/VM onde a aplicação ficará rodando  
- Dependências listadas no arquivo `requirements.txt`

## Funcionamento

1. A aplicação permanece em modo de escuta, aguardando a entrada de um código (via leitor QR/Código de Barras).  
2. Ao receber uma entrada, realiza uma consulta no banco de dados para validar o dado recebido.  
3. Se validado com sucesso, a aplicação aciona o equipamento Control ID via API para permitir a saída da pessoa ou veículo.

## Instalação

Clone este repositório:

```bash
git clone https://github.com/CharlitonJ/Leitura-QRCODE-MySQL-ControlID.git
cd Leitura-QRCODE-MySQL-ControlID
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Usar

1. Configure o arquivo `config.ini` com as credenciais e parâmetros do seu ambiente (banco de dados e Control ID).  
2. Execute o script principal:

```bash
python script.py
```

## Projeto Privado

Este é um projeto privado e não possui licenciamento público.  
Uso ou redistribuição sem autorização do autor é proibido.

## Autor

- Charliton Junior  
- GitHub: https://github.com/CharlitonJ  
- LinkedIn: https://www.linkedin.com/in/charliton-junior/
