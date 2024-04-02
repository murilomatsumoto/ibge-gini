from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sua_base_de_dados import Base, Brasil, Estado, Cidade

class ManipuladorDadosGini:
    def __init__(self, db_path):
        """Inicializa o manipulador de dados com o caminho do banco de dados."""
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def adicionar_estado_e_cidades(self, nome_estado, indice_gini_brasil, dados_cidades):
        """Adiciona um estado e suas cidades ao banco de dados."""
        session = self.Session()
        
        try:
            brasil = session.query(Brasil).filter_by(Indice_Gini_1991=indice_gini_brasil).first()
            if not brasil:
                brasil = Brasil(Indice_Gini_1991=indice_gini_brasil)
                session.add(brasil)
                session.commit()

            estado = Estado(Nome_estado=nome_estado, brasil=brasil)
            session.add(estado)
            session.commit()

            for cidade, indice_gini_cidade in dados_cidades.items():
                nova_cidade = Cidade(Nome_cidade=cidade, ID_estado=estado.ID_estado, Indice_Gini_1991=indice_gini_cidade)
                session.add(nova_cidade)
            session.commit()

            print(f"Estado {nome_estado} e suas cidades foram adicionados com sucesso ao banco de dados.")
        except Exception as e:
            print(f"Ocorreu um erro ao adicionar o estado e suas cidades: {str(e)}")
        finally:
            session.close()

# Exemplo de uso da classe
dados_cidades_acre = {
    'Acrelândia': 0.61,
    'Assis Brasil': 0.4517,
    'Brasiléia': 0.5331,
    # Adicione mais cidades do Acre conforme necessário
}

manipulador = ManipuladorDadosGini('dados_gini.db')
manipulador.adicionar_estado_e_cidades('Acre', 0.6366, dados_cidades_acre)
