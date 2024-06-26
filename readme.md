# Extração do índice de Gini - IBGE

**Esse projeto consiste na elaboração de webscraping para extração dos arquivos .zip do site do ibge, extraindo as informações do índice de Gini de cada cidade e estado, armazendo em um banco de dados SQLite**


## Processo de instalação local

```bash
  git clone https://github.com/murilomatsumoto/ibge-gini.git
  python -m venv venv
    - Ative seu ambiente virtual*
  pip install -r requirements.txt
```

## Variáveis 

`CHROME_DRIVER_LOCAL` = Chromedriver para execução do chrome (Verificar compatiblidade com o chrome instalado na máquina que será executado o código) - Versão utilizada no projeto: 123.0.6312.86
https://googlechromelabs.github.io/chrome-for-testing/#stable

`LOCAL_PATH` = /Path - Caminho completo da pasta src/downloads/zip (Armazenamento temporário dos arquivos .zip)

        src
            ├── constants
            │   └── names.py

As variáveis deverão ser inseridas no arquivo names.py

--------

## How to run (local):
**main.py**   

Rode o arquivo main.py
O scraping de dados comecará automaticamente, onde os dados serão armazenados no banco de dados SQlite "dados_gini.db"

------
## *Processo de criação de container - Docker*

#### Obs: O processo de criação consiste na criação do container com a instalação do google-chrome-stable. Sugere-se que a criação seja realizada em uma ambiente Linux. (Não compatível com M1 Macbook)

```bash
  git clone https://github.com/murilomatsumoto/ibge-gini.git
```
Vá para a raiz do projeto:

```bash
  docker build -t <nome_da_imagem> .
```
Com a imagem já criada, está na hora de rodar o container:

- Para rodar o projeto:
```bash
  docker run -it <nome_da_imagem>    
```
- Para rodar o container e acessar seu terminal:
```bash
  docker run -it <nome_da_imagem> /bin/bash
```
-------
## Banco de dados

- Visualização das tabelas criadas no banco de dados:

![Exemplo de Imagem](tabelas.png)

- No  arquivo result_cidades.json é possível verificar os resultados do scraping
- Obs: Nos casos em que não foi encontrado o índice, foi considerado null

  - Exemplo:

        {
          "ID_cidade" : 1,
          "ID_estado" : 1,
          "Nome_cidade" : "Acrelândia",
          "Indice_Gini_1991" : null
        },
        {
          "ID_cidade" : 2,
          "ID_estado" : 1,
          "Nome_cidade" : "Assis Brasil",
          "Indice_Gini_1991" : 0.4517
        }

--------


For suport, send e-mail to murilomatsumoto@gmail.com.