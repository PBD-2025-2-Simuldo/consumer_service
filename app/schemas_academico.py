from pydantic import BaseModel, Field, validator
from typing import List, Optional

class DisciplinaBase(BaseModel):
    nome: str

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaOut(DisciplinaBase):
    id: int
    class Config:
        orm_mode = True

class AssuntoBase(BaseModel):
    nome: str
    disciplina_id: int

class AssuntoCreate(AssuntoBase):
    pass

class AssuntoOut(AssuntoBase):
    id: int
    class Config:
        orm_mode = True

class QuestaoBase(BaseModel):
    descricao: str
    dificuldade: int = Field(..., ge=1, le=3)
    tipo: str
    disciplina_id: int
    assuntos: List[int] = []

    @validator("tipo")
    def validar_tipo(cls, v):
        if v not in ("unica", "multipla"):
            raise ValueError("tipo deve ser 'unica' ou 'multipla'")
        return v

class QuestaoCreate(QuestaoBase):
    pass

class QuestaoOut(BaseModel):
    id: int
    descricao: str
    dificuldade: int
    tipo: str
    disciplina_id: int
    assuntos: List[AssuntoOut] = []

    class Config:
        orm_mode = True
