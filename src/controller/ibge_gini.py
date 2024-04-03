from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from services.file_service import Uteis
import os
from log.loggin_utils import Log
from selenium.webdriver.chrome.service import Service
from constants.names import LOCAL_PATH, CHROMEDRIVER_PATH, LOCAL_PATH_DOCKER, CHROME_DRIVER_LOCAL
from webdriver_manager.chrome import ChromeDriverManager



log = Log()

class Scraping:
    
    @staticmethod
    def scraping_ibge():
        options = webdriver.ChromeOptions()
        download_path = LOCAL_PATH_DOCKER
        options.add_argument('--headless')      
        options.add_argument('--no-sandbox') 
        options.add_argument('--disable-dev-shm-usage') 
        options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
        # chrome_driver_path = ChromeDriverManager().install()
        chrome_driver_path = CHROMEDRIVER_PATH
        chrome_service = Service(executable_path=chrome_driver_path, log_path='/tmp/chromedriver.log')
        driver = webdriver.Chrome(options=options, service=chrome_service)
        

        url = "https://www.ibge.gov.br/"
        driver.get(url)

        menu = driver.find_element(By.XPATH, '//a[@id="nav-toggle" and contains(@class, "")]')
        if menu:
            try:
                log.log_message('Menu principal encontrado, acessando subitens')
                menu.click()
                sleep(1)
            except:
                driver.execute_script('arguments[0].click();', menu) 
            estatisticas_element = driver.find_element(By.XPATH, '//li[@idmenu="1" and @class="parent nvcls_"]')
            if estatisticas_element:
                log.log_message('Clicando em estatísticas')
                estatisticas_element.click()
                downloads_element = driver.find_element(By.XPATH, '//li[@idmenu="36" and @class=" nvcls_"]')
                if downloads_element:
                    log.log_message('Acessando a área de Downloads')
                    downloads_element.click()
                    
                    WebDriverWait(driver, 10).until(
                        EC.url_contains('downloads')
                    )
                            
        censo_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Censos_anchor'))     
                )
                        
        censo_element = driver.find_element(By.ID, 'Censos_anchor')
        if censo_element:
            censo_element.click()
            log.log_message('Clicando em Censo')
            censo_noventa_um_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991_anchor"]')
            if censo_noventa_um_element:
                censo_noventa_um_element.click()
                log.log_message('Acessando censo de 1991')
                indice_gini_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"]/i'))
                    )     
                indice_gini_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"]/i')

                if indice_gini_element:
                    try:
                        indice_gini_element.click()    
                    except:
                        driver.execute_script('arguments[0].click();', indice_gini_element) 
                        log.log_message('Acessando o índice gini')
                    estados_tag = driver.find_elementindice_gini_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"]/ul')
                    if estados_tag:
                        itens_download = estados_tag.find_elements(By.TAG_NAME, 'li')
                        log.log_message('Elementos .zip encontrados para download')
                        for element in itens_download:
                            link_produto = element.find_element(
                                By.XPATH, './/a[@href]')
                            if link_produto:
                                file_zip = link_produto.text
                            try:
                                link_produto.click()
                            except:
                                driver.execute_script('arguments[0].click();', link_produto) 
                                log.log_message('Acessando área do link')
                            link_produto2 = link_produto.find_element(
                                By.XPATH, './/i[@class]')
                            try:
                                link_produto2.click()
                            except:
                                driver.execute_script('arguments[0].click();', link_produto2) 
                                log.log_message(f'Realizando o download do .zip {file_zip}')
                                
                            path_to_unzip = f'{download_path}/{file_zip}'
                            Uteis.unzip_file(path_to_unzip, 'src/downloads/xls')

                            arquivo_xls = Uteis.buscar_arquivo_excel()
                            log.log_message(f'Arquivo {arquivo_xls} encontrado para extração das informações')
                            if arquivo_xls:
                                Uteis.leitura_excel_insert_db(arquivo_xls)
                                if not 'Leia_me.txt' in arquivo_xls:
                                    os.remove(path_to_unzip)
                                    log.log_message(f'Removendo arquivo temporário {path_to_unzip}')
                                    os.remove(arquivo_xls)
                                    log.log_message(f'Removendo arquivo temporário {arquivo_xls}')

                            
                            
                        
        driver.quit()

