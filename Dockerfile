# Use a imagem oficial do Python
FROM openjdk:17.0.2-slim-bullseye
# FROM ubuntu

# Install System Dependencies
RUN apt-get update\
    && apt-get -y install ca-certificates wget curl gnupg2 unzip --no-install-recommends \
    && curl -L https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -qqy \
    && apt-get -qqy install ${CHROME_VERSION:-google-chrome-stable} \
    && apt-get -f install \
    && apt-get clean \
    && rm /etc/apt/sources.list.d/google-chrome.list \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*


# Baixe o arquivo zip do ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/123.0.6309.0/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /opt/chrome \
    && mv /opt/chrome/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver-linux64.zip

  # Install System Dependencies
RUN apt-get update && \
     \
    apt-get -y install python3.9 python3.9-venv libgl1-mesa-glx \
    python3-pip \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /src

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte da aplicação para o diretório de trabalho
COPY /src .

# RUN set -xe && apt-get -yqq update && apt-get -yqq install python3-pip && pip3 install --upgrade pip

# Exemplo de comando para rodar o script do Selenium (substitua pelo seu próprio comando)
CMD ["python3", "main.py"]
