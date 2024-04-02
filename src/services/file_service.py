import zipfile
import os


class Uteis:
    @staticmethod
    def unzip_file(file_path, extract_to):
        """
        Unzips a file to a specified directory.

        Parameters:
        file_path (str): The path to the ZIP file.
        extract_to (str): The directory where the contents of the ZIP file will be extracted.
        """
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Arquivo {file_path} não encontrado.")
            return
        
        # Verifica se o arquivo é um arquivo ZIP
        if not zipfile.is_zipfile(file_path):
            print(f"O arquivo {file_path} não é um arquivo ZIP válido.")
            return
        
        # Extrai o conteúdo do arquivo ZIP
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Arquivo {file_path} descompactado com sucesso para {extract_to}.")
