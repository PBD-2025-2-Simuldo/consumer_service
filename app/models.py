from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

questao_assunto = Table(
    "questao_assunto",
    Base.metadata,
    Column("questao_id", Integer, ForeignKey("questoes.id"), primary_key=True),
    Column("assunto_id", Integer, ForeignKey("assuntos.id"), primary_key=True),
)

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)

    assuntos = relationship("Assunto", back_populates="disciplina", cascade="all, delete-orphan")

class Assunto(Base):
    __tablename__ = "assuntos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)

    disciplina = relationship("Disciplina", back_populates="assuntos")
    questoes = relationship("Questao", secondary=questao_assunto, back_populates="assuntos")

class Questao(Base):
    __tablename__ = "questoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(Text, nullable=False)
    dificuldade = Column(Integer, nullable=False)  # 1,2,3
    tipo = Column(String, nullable=False)  # 'unica' ou 'multipla'
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)

    disciplina = relationship("Disciplina")
    assuntos = relationship("Assunto", secondary=questao_assunto, back_populates="questoes")
