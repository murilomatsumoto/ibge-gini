from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Brasil(Base):
    __tablename__ = "brasil"

    ID_brasil = Column(Integer, primary_key=True)
    Indice_Gini_1991 = Column(Float)


class Estado(Base):
    __tablename__ = "estado"

    ID_estado = Column(Integer, primary_key=True)
    ID_brasil = Column(Integer, ForeignKey("brasil.ID_brasil"))
    Nome_estado = Column(String)
    Indice_Gini_1991 = Column(Float)
    brasil = relationship("Brasil")


class Cidade(Base):
    __tablename__ = "cidade"

    ID_cidade = Column(Integer, primary_key=True)
    ID_estado = Column(Integer, ForeignKey("estado.ID_estado"))
    Nome_cidade = Column(String)
    Indice_Gini_1991 = Column(Float)


engine = create_engine("sqlite:///dados_gini.db")

# Base.metadata.create_all(engine)
