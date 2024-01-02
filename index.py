import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np

def web_scraping(url, id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    table = driver.find_element('id', id)
    table_html = table.get_attribute('outerHTML')
    return table_html

df = pd.read_html(web_scraping("https://www.fundamentus.com.br/resultado.php", 'resultado'))[0]
df = df[['Papel', 'P/L', 'P/VP', 'Div.Yield', 'EV/EBIT', 'Liq. Corr.', 'ROIC', 'ROE', 'Liq.2meses', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a']]

cols_to_divide = ['P/L', 'P/VP', 'EV/EBIT', 'Liq. Corr.', 'Liq.2meses', 'Dív.Brut/ Patrim.']
for col in cols_to_divide:
    df[col] = df[col].astype(str).str.replace('.', '').str.replace(',', '').astype(float) / 100

cols_to_porcent = ['Div.Yield', 'ROIC', 'ROE', 'Cresc. Rec.5a']
for col in cols_to_porcent:
    df[col] = df[col].astype(str).str.replace('%', '').str.replace('.', '').str.replace(',', '').astype(float) / (100*100)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./service_account.json', scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key('1otfLq22CPlr5hpQU5bINpEIbb2trx-UF3klHj0w45zE')
worksheet = spreadsheet.worksheet('AÇÕES')

worksheet.clear()
column_names = df.columns.values.tolist()
worksheet.insert_row(column_names, 1)
worksheet.insert_rows(df.values.tolist(), 2)

df1 = pd.read_html(web_scraping("https://www.fundamentus.com.br/fii_resultado.php", 'tabelaResultado'))[0]
df1 = df1[['Papel', 'Segmento', 'FFO Yield', 'Dividend Yield', 'P/VP', 'Valor de Mercado', 'Liquidez', 'Qtd de imóveis', 'Vacância Média']]

cols_to_divide_fii = ['P/VP', 'Valor de Mercado', 'Liquidez']
for col in cols_to_divide_fii:
    df1[col] = df1[col].astype(str).str.replace('.', '').str.replace(',', '').astype(float) / 100

cols_to_porcent_fii = ['FFO Yield', 'Dividend Yield', 'Vacância Média']
for col in cols_to_porcent_fii:
    df1[col] = df1[col].astype(str).str.replace('%', '').str.replace('.', '').str.replace(',', '').astype(float) / (100*100)

df1['Qtd de imóveis'] = df1['Qtd de imóveis'].astype(int)
df1['Segmento'] = df1['Segmento'].astype(str)

spreadsheet = client.open_by_key('1otfLq22CPlr5hpQU5bINpEIbb2trx-UF3klHj0w45zE')
worksheet_fii = spreadsheet.worksheet('FII')
worksheet_fii.clear()
column_names_fii = df1.columns.values.tolist()
worksheet_fii.insert_row(column_names_fii, 1)
worksheet_fii.insert_rows(df1.values.tolist(), 2)
