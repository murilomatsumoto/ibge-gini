import zipfile
import os
import re
import pandas as pd
from models.repository.connection_sqlite import ManipuladorDB
from log.loggin_utils import Log

log = Log()


class Uteis:
    @staticmethod
    def unzip_file(file_path, extract_to):

        if not os.path.exists(file_path):
            print(f"Arquivo {file_path} não encontrado.")
            return

        if not zipfile.is_zipfile(file_path):
            print(f"O arquivo {file_path} não é um arquivo ZIP válido.")
            return

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Arquivo {file_path} descompactado com sucesso para {extract_to}.")

    @staticmethod
    def extrair_nome_cidade(nome_cidade):
        match = re.match(r"(.+?)\s*-\s*\w+", nome_cidade)
        if match:
            return match.group(1)
        else:
            return nome_cidade

    @staticmethod
    def leitura_excel_insert_db(file_path):
        # Ler o arquivo Excel
        df = pd.read_excel(file_path, index_col=0)

        # Iterar sobre as linhas e índices do DataFrame
        for idx, (index, row) in enumerate(df.iterrows()):
            if idx == 0:
                print("Nome do país:", index)
                log.log_message(f"Nome do país: {index}")
            elif idx == 1:
                print("Nome do estado:", index)
                log.log_message(f"Nome do estado: {index}")
            else:
                try:
                    nome_cidade = Uteis.extrair_nome_cidade(index)
                    print("Nome da cidade:", nome_cidade)
                    log.log_message(f"Nome da cidade: {nome_cidade}")
                except TypeError:
                    print(
                        "Sem cidade, passando para próxima informação. OBS: Inconformidade na planilha"
                    )
                    continue

            # Iterar sobre as colunas e valores da linha
            for column, value in row.items():
                if not pd.isna(value):  # Verificar se o valor não é NaN
                    if value == "...":
                        value = None
                    print("Ano:", column)
                    log.log_message(f"Ano: {column}")
                    print("Índice Gini:", value)
                    log.log_message(f"Índice Gini: {value}")
                    print("-----------------")
                    log.log_message("-----------------")

                    if idx == 0:
                        brasil = ManipuladorDB().inserir_brasil(value)
                    elif idx == 1:
                        estado = ManipuladorDB().adicionar_estado(index, value, brasil)
                    else:
                        ManipuladorDB().adicionar_cidade(
                            nome_cidade=nome_cidade, indice_gini=value, id_estado=estado
                        )

    @staticmethod
    def buscar_arquivo_excel():
        diretorio = os.path.join("src/downloads", "xls")
        if not os.path.exists(diretorio):
            log.log_message("O diretório 'xls' não existe em src/downloads")
            return None

        arquivos = [
            arq
            for arq in os.listdir(diretorio)
            if arq.lower().endswith(".xls") or arq.lower().endswith(".XLS")
        ]
        if not arquivos:
            log.log_message(f"Nenhum arquivo Excel encontrado na pasta {diretorio}")
            return None

        return os.path.join(diretorio, arquivos[0])
