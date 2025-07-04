from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Tabela(Base):
    __tablename__ = 'tabela'

    id = Column(Integer, primary_key=True)
    codigo = Column(String, unique=True, nullable=False)
    descricao = Column(Text, nullable=False)

    colunas = relationship("Coluna", back_populates="tabela", cascade="all, delete-orphan")


class Coluna(Base):
    __tablename__ = 'coluna'

    id = Column(Integer, primary_key=True)
    tabela_id = Column(Integer, ForeignKey('tabela.id'), nullable=False)
    codigo_coluna = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

    tabela = relationship("Tabela", back_populates="colunas")
