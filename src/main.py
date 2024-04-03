from controller.ibge_gini import Scraping
import os
from constants.names import (
    LOCAL_PATH,
    CHROMEDRIVER_PATH_DOCKER,
    LOCAL_PATH_DOCKER,
    CHROME_DRIVER_LOCAL,
)


def main():
    if os.path.exists(CHROMEDRIVER_PATH_DOCKER):
        Scraping(
            driver_path=CHROMEDRIVER_PATH_DOCKER, download_path=LOCAL_PATH_DOCKER
        ).scraping_ibge()
        print("Acesso via Docker")
    else:
        Scraping(
            driver_path=CHROME_DRIVER_LOCAL, download_path=LOCAL_PATH
        ).scraping_ibge()
        print("Acesso local")


if __name__ == "__main__":
    main()
