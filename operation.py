from Helpers import webdriver, Options, sleep, By

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

def getAcaoInformations(ticker):
    url = f"https://statusinvest.com.br/acoes/{ticker}"
    driver.get(url)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

def getSummaryAcao(acao):
    resumo = {}
    for x, y in enumerate(acao):
        driver.switch_to.window(driver.window_handles[x])
        data_acao = [driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[1]/div/div[1]/strong').text,
        driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[2]/div/div[1]/strong').text,
        driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[3]/div/div[1]/strong').text,
        driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong').text,
        driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[1]/strong').text]
        resumo[y] = data_acao

    return resumo

def getValuationAcao(acao):
    indicadores = {}
    for x, y in enumerate(acao):
        driver.switch_to.window(driver.window_handles[x])
        data_acao = {}
        for _ in range(1, 15):
            try:
                indicator_name = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[{_}]/div/h3').text.lower().replace(' ', '_').replace('.', '')
            except Exception as e:
                indicator_name = driver.find_element(By.XPATH, f'/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[{_}]/div/a/h3').text.lower().replace(' ', '_').replace('.', '')
            data_acao[indicator_name] = (driver.find_element(By.XPATH, f'/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[{_}]/div/div/strong').text)
        indicadores[y] = data_acao

    return indicadores
