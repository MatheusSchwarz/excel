
#Importando as bibliotecas que serÃ£o utilizadas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

#Importando a tabela com os links
local_pasta = '/root/webscrapping/excel/links_precos.xlsx'
df = pd.read_excel(local_pasta)

salvar_excel = '/root/webscrapping/excel/webscraping.xlsx'
df.to_excel(salvar_excel)

#Definindo a variável j como global
global j

#Abrindo o navegador
driver = webdriver.Chrome()

# -----WEB SCRAPING AMAZON-----
j=0

for pagina in df['Amazon']:
    try:
        driver.get(pagina)
        time.sleep(4)
        
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        
        try:
            valor = site.find('span', class_='olpWrapper a-size-small').get_text().replace("R$",'')
            df.loc[j,'Preço Amazon'] = valor
            j +=1
        except:
            valor_inteiro = site.find('span', 'a-price-whole').get_text()
            valor_centavos = site.find('span', 'a-price-fraction').get_text()
            valor = valor_inteiro+valor_centavos
            df.loc[j,'Preço Amazon'] = valor
            j +=1
        
    except:
        df.loc[j,'Preço Amazon'] = "Não encontrado"
        j+=1
        

# -----WEB SCRAPING LOJA INTELBRAS-----
j=0

for pagina in df['Loja Intelbras']:
    try:
        driver.get(pagina)
        time.sleep(2)
        
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        
        valor = site.find('span', 'vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--pdp--sellingPrice').get_text().replace("R$ ",'')
        df.loc[j,'Preço Loja Intelbras'] = valor
        j+=1
        
    except:
        df.loc[j,'Preço Loja Intelbras'] = "Não encontrado"
        j+=1

# -----WEB SCRAPING MERCADO LIVRE-----
j=0

for pagina in df['Mercado Livre']:
    try:
        driver.get(pagina)
        time.sleep(3)
    
        html = driver.page_source
        site = BeautifulSoup(html, 'html.parser')
        
        valor = site.find('span', class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').get_text().replace("R$",'')
    
        df.loc[j,'Preço Mercado Livre'] = valor
        j +=1
        
    except:
        df.loc[j,'Preço Mercado Livre'] = "Não encontrado"
        j+=1
        
# -----WEB SCRAPING GOOGLE-----
j=0

for pagina in df['Título']:
    driver.get('https://shopping.google.com.br/')
    time.sleep(2)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(pagina)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    
    html = driver.page_source
    site = BeautifulSoup(html, 'html.parser')
    
    
    #Procura os produtos caso apareça na página "Melhor Correspondência"
    try:
        valor = float(site.find('span', class_='_-p3 _-pZ').get_text().replace('R$ ','').replace('.','').replace(',','.'))
        produtos = site.find_all('div', class_='_-oz')
        descricao = site.find('div', class_='_-pg').get_text()        
        
        
        for produto in produtos:
            valor_produto = float(produto.find('span', class_='_-p3 _-pZ').get_text().replace('R$ ','').replace('.','').replace(',','.'))
            
            if valor_produto <= valor:
                valor = valor_produto
                vendedor = produto.find('div', class_='_-oF _-oD').get_text()
                link = 'www.google.com.br'+produto.find('a', class_='_-oA shntl').get('href')
                
                df.loc[j,'Preço Google'] = valor
                df.loc[j,'Vendedor Google'] = vendedor
                df.loc[j,'Descrição Produto Google'] = descricao
                df.loc[j,'Link produto Goole'] = link
            else:
                pass        
    
    #Caso não encontre "Melhor Correspondência", procura na parte de "Patrocinados"
    except:
        try:
            valor = float(site.find('b', class_='translate-content').get_text().replace('R$ ','').replace('.','').replace(',','.'))                
            produtos = site.find_all('div', class_='KZmu8e')
            
            for produto in produtos:
                valor_produto = float(produto.find('b', class_='translate-content').get_text().replace('R$ ','').replace('.','').replace(',','.'))
                if valor_produto <= valor:
                    valor = valor_produto
                    vendedor = produto.find('span',class_='E5ocAb').get_text()
                    try:
                        descricao = produto.find('h3', class_='sh-np__product-title translate-content').get_text()
                    except:
                        descricao = produto.find('h3', class_='sh-np__product-title-visited-link sh-np__product-title translate-content').get_text()
                    link = 'www.google.com.br'+produto.find('a', class_='shntl sh-np__click-target').get('href')
                    
                    df.loc[j,'Preço Google'] = valor
                    df.loc[j,'Vendedor Google'] = vendedor
                    df.loc[j,'Descrição Produto Google'] = descricao
                    df.loc[j,'Link produto Goole'] = link
                else:
                    pass
        #Se não encontrar os produtos em "Melhor Correspondência" ou "Patrocinados", preencha com  "-"
        except:
            df.loc[j,'Preço Google'] = 'Não encontrado produtos em "Melhor Correspondência" ou "Patrocinado"'
            df.loc[j,'Vendedor Google'] = '-'
            df.loc[j,'Descrição Produto Google'] = '-'
            df.loc[j,'Link produto Goole'] = '-'
            pass
    j+=1
    
df.to_excel(salvar_excel)

    


    

    