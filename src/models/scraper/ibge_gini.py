from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
    

    driver.quit()

if __name__ == "__main__":
    main()
