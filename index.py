from Helpers import sleep
from operation import *

my_acoes = ['VALE3', 'BBAS3', 'KLBN11', 'CMIG4', 'BBSE3', 'CXSE3', 'TASA3', 'PETR4', 'BAZA3']

for _ in my_acoes:
    getAcaoInformations(_)



sleep(100)

driver.quit()
