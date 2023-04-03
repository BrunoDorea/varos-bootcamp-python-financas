import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Passo 2 - Pegando dados do Yahoo Finance
ativos = ['^BVSP', 'BRL=X', 'ITSA4.SA']
hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days=365)
dados_mercados = yf.download(ativos, um_ano_atras, hoje)

# print(dados_mercados)

# Passo 3.1 - Manipulando os dados - seleção e exclusão de dados
dados_fechamento = dados_mercados['Adj Close']
dados_fechamento.columns = ['ibovespa', 'dolar', 'itausa']
dados_fechamento = dados_fechamento.dropna()

# print(dados_fechamento)

# Passos 3.2 - Manipulando os dados - criando tabelas com outros timeframes
dados_fechamento_mensal = dados_fechamento.resample("M").last()
dados_fechamento_anual = dados_fechamento.resample("Y").last()

# print(dados_fechamento_mensal)
# print(dados_fechamento_anual)

# Passo 4 - Calcular o fechamento do dia, retorno do ano e retorno no mês dos ativos
retorno_no_ano = dados_fechamento_anual.pct_change().dropna()
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()
retorno_no_dia = dados_fechamento.pct_change().dropna()

# print(retorno_no_dia)

# Passo 5 - Localizar o fechamento do dia anterior, retorno do mês e retorno do ano
retorno_dia_dolar = round(retorno_no_dia.iloc[-1, 0] * 100, 2)
retorno_dia_ibovespa = round(retorno_no_dia.iloc[-1, 1] * 100, 2)
retorno_dia_itausa = round(retorno_no_dia.iloc[-1, 2] * 100, 2)

retorno_mes_dolar = round(retorno_no_mes.iloc[-1, 0] * 100, 2)
retorno_mes_ibovespa = round(retorno_no_mes.iloc[-1, 1] * 100, 2)
retorno_mes_itausa = round(retorno_no_mes.iloc[-1, 2] * 100, 2)

retorno_ano_dolar = round(retorno_no_ano.iloc[-1, 0] * 100, 2)
retorno_ano_ibovespa = round(retorno_no_ano.iloc[-1, 1] * 100, 2)
retorno_ano_itausa = round(retorno_no_ano.iloc[-1, 2] * 100, 2)

# print(retorno_dia_ibovespa, retorno_dia_dolar, retorno_dia_itausa)

# Passo 6 - Gerar os gráficos da performance do último dos ativos
plt.style.use('cyberpunk')
dados_fechamento.plot(y='dolar', use_index=True, legend=False)
plt.title('Dólar')
plt.savefig('dolar.png', dpi=300)
plt.show()

plt.style.use('cyberpunk')
dados_fechamento.plot(y='itausa', use_index=True, legend=False)
plt.title('Itau')
plt.savefig('itausa.png', dpi=300)
plt.show()

plt.style.use('cyberpunk')
dados_fechamento.plot(y='ibovespa', use_index=True, legend=False)
plt.title('Ibovespa')
plt.savefig('ibovespa.png', dpi=300)
plt.show()

# Passo 7 - Enviar email
load_dotenv()
senha = os.environ.get("senha")
email = os.environ.get("email")

msg = EmailMessage()
msg['Subject'] = "Relatório de Fechamento de Mercado com Python - Bruno Henrique"
msg['From'] = os.environ.get("email")
msg['To'] = 'brunodorea@outlook.com.br'
msg['To'] = 'brenno@varos.com.br'
msg.set_content(f'''Prezados, segue o relatório diário:

Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_ibovespa}%, 
enquanto no mês a rentabilidade é de {retorno_mes_ibovespa}%.
No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_ibovespa}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%, 
enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.
No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.

Itaú SA:

No ano o Itaú SA está tendo uma rentabilidade de {retorno_ano_itausa}%, 
enquanto no mês a rentabilidade é de {retorno_mes_itausa}%.
No último dia útil, o fechamento do Itaú SA foi de {retorno_dia_itausa}%.

Att,

Bruno Dórea
https://brunodorea.gatsbyjs.io/

''')

with open('dolar.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='dolar.png')

with open('itausa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='itausa.png')

with open('ibovespa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application', subtype='png', filename='ibovespa.png')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, senha)
    smtp.send_message(msg)
