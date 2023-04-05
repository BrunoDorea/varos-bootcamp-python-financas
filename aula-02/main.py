from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.etf.com/etfanalytics/etf-finder')

time.sleep(10)
btn_100 = driver.find_element("xpath", "/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[1]/div/div[4]/button/label/span")
btn_100.click()
#driver.execute_script("arguments[0].click", btn_100)

# Passo 5.2 - Encontrar todos elementos necessários dentro do site
numero_paginas = driver.find_element("xpath", "/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[2]/div/label[2]")
numero_paginas = numero_paginas.text.replace("of ", "")
numero_paginas = int(numero_paginas)

# Passo 6.1 - Ler a tabela de dados
lista_tabela_por_pagina = []
elemento = driver.find_element("xpath", '//*[@id="finderTable"]')

for pagina in range(1, numero_paginas):
    html_tabela = elemento.get_attribute('outerHTML')
    tabela = pd.read_html(str(html_tabela))[0]
    lista_tabela_por_pagina.append(tabela)
    btn_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
    driver.execute_script("arguments[0].click", btn_avancar_pagina)

tabela_cadastro_etfs = pd.concat(lista_tabela_por_pagina)

# Passo 6.2 Preencher um campo no site para voltar as páginas
formulario_btn_pagina = driver.find_element("xpath", '//*[@id="goToPage"]')
formulario_btn_pagina.clear()
formulario_btn_pagina.send_keys("1")
formulario_btn_pagina.send_keys(u'\ue007')

# Passo 6.3 - Ler a tabela de dados
btn_performance = driver.find_element("xpath", '/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/ul/li[2]/span')
btn_performance.click()

lista_tabela_por_pagina = []
elemento = driver.find_element("xpath", '//*[@id="finderTable"]')

for pagina in range(1, numero_paginas):
    html_tabela = elemento.get_attribute('outerHTML')
    tabela = pd.read_html(str(html_tabela))[0]
    lista_tabela_por_pagina.append(tabela)
    btn_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
    driver.execute_script("arguments[0].click", btn_avancar_pagina)

tabela_rentabilidade_etfs = pd.concat(lista_tabela_por_pagina)

driver.quit()

tabela_rentabilidade_etfs = tabela_rentabilidade_etfs.set_index("Ticker")
tabela_rentabilidade_etfs = tabela_rentabilidade_etfs[['1 Year', '3 Years', '5 Years']]

tabela_cadastro_etfs = tabela_cadastro_etfs.set_index("Ticker")

base_dados_final = tabela_cadastro_etfs.join(tabela_rentabilidade_etfs, how='inner')
