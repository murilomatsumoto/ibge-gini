from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.entities.tables import Base, Brasil, Estado, Cidade
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from log.loggin_utils import Log

log = Log()


class ManipuladorDB:
    def __init__(self):
        self.engine = create_engine('sqlite:///dados_gini.db')
        Base.metadata.create_all(self.engine)

    def inserir_brasil(self, indice_gini):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            existing_entry = session.query(Brasil).filter_by(Indice_Gini_1991=indice_gini).first()

            if existing_entry:
                log.log_message("O índice Gini já está presente na tabela Brasil. Não foi realizada nenhuma inserção.")
                return existing_entry.ID_brasil
            else:
                brasil_entry = Brasil(Indice_Gini_1991=indice_gini)
                session.add(brasil_entry)
                session.commit()
                log.log_message("Dados inseridos na tabela Brasil com sucesso!")
                return brasil_entry.ID_brasil

        except IntegrityError as e:
            log.log_message(f"Erro de integridade ao inserir dados na tabela Brasil: {str(e)}")
            session.rollback()
            return None
        except Exception as e:
            log.log_message(f"Erro ao inserir dados na tabela Brasil: {str(e)}")
            return None
        finally:
            session.close()
            
    def adicionar_estado(self, nome_estado, indice_gini, id_brasil):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            existing_state = session.query(Estado).filter_by(Nome_estado=nome_estado).first()

            if existing_state:
                log.log_message(f"O estado {nome_estado} já está presente na tabela Estado. Não foi realizada nenhuma inserção.")
                return existing_state.ID_estado
            else:
                brasil = session.query(Brasil).filter_by(ID_brasil=id_brasil).first()

                if brasil:
                    estado_entry = Estado(Nome_estado=nome_estado, Indice_Gini_1991=indice_gini, ID_brasil=id_brasil)
                    session.add(estado_entry)
                    session.commit()
                    log.log_message(f"Dados do estado {nome_estado} inseridos na tabela Estado com sucesso!")
                    return estado_entry.ID_estado
                else:
                    log.log_message(f"Não foi possível encontrar o Brasil com o ID {id_brasil}. Nenhuma inserção foi realizada.")
                    return None

        except IntegrityError as e:
            log.log_message(f"Erro de integridade ao inserir dados na tabela Estado: {str(e)}")
            session.rollback()
            return None
        except Exception as e:
            log.log_message(f"Erro ao inserir dados na tabela Estado: {str(e)}")
            return None
        finally:
            session.close()
            
    def adicionar_cidade(self, nome_cidade, indice_gini, id_estado):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            existing_city = session.query(Cidade).filter_by(Nome_cidade=nome_cidade).first()

            if existing_city:
                log.log_message(f"A cidade {nome_cidade} já está presente na tabela Cidade. Não foi realizada nenhuma inserção.")
                return existing_city.ID_cidade
            else:
                estado = session.query(Estado).filter_by(ID_estado=id_estado).first()

                if estado:
                    cidade_entry = Cidade(Nome_cidade=nome_cidade, Indice_Gini_1991=indice_gini, ID_estado=id_estado)
                    session.add(cidade_entry)
                    session.commit()
                    log.log_message(f"Dados da cidade {nome_cidade} inseridos na tabela Cidade com sucesso!")
                    return cidade_entry.ID_cidade
                else:
                    log.log_message(f"Não foi possível encontrar o estado com o ID {id_estado}. Nenhuma inserção foi realizada.")
                    return None

        except IntegrityError as e:
            log.log_message(f"Erro de integridade ao inserir dados na tabela Cidade: {str(e)}")
            session.rollback()
            return None
        except Exception as e:
            log.log_message(f"Erro ao inserir dados na tabela Cidade: {str(e)}")
            return None
        finally:
            session.close()


