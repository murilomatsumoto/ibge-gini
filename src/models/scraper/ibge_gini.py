from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main():
    options = Options()
    # options.headless = True  
    driver = Chrome(options=options)

    url = "https://www.ibge.gov.br/"
    driver.get(url)

    menu = driver.find_element(By.XPATH, '//a[@id="nav-toggle" and contains(@class, "")]')
    if menu:
        print('menu encontrado')
        menu.click()
        sleep(1)
        estatisticas_element = driver.find_element(By.XPATH, '//li[@idmenu="1" and @class="parent nvcls_"]')
        if estatisticas_element:
            estatisticas_element.click()
            downloads_element = driver.find_element(By.XPATH, '//li[@idmenu="36" and @class=" nvcls_"]')
            if downloads_element:
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
        censo_noventa_um_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991_anchor"]')
        if censo_noventa_um_element:
            censo_noventa_um_element.click()
            sleep(5)
            indice_gini_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"]/i')

            if indice_gini_element:
                try:
                    indice_gini_element.click()    
                except:
                    driver.execute_script('arguments[0].click();', indice_gini_element) 
                    print('ok')
                estados_tag = driver.find_elementindice_gini_element = driver.find_element(By.XPATH, '//li[@aria-labelledby="Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"]/ul')
                if estados_tag:
                    itens_download = estados_tag.find_elements(By.TAG_NAME, 'li')
                    for item in itens_download:
                        print(item.text)
                    
    driver.quit()

if __name__ == "__main__":
    main()
