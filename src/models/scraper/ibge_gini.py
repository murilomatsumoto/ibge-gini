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
                     EC.presence_of_element_located((By.CLASS_NAME, "conteudo__interna__titulo pure-u-1")))
        
    
    driver.quit()

if __name__ == "__main__":
    main()
