from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.schemas_academico import (
    DisciplinaCreate, DisciplinaOut,
    AssuntoCreate, AssuntoOut,
    QuestaoCreate, QuestaoOut
)

router = APIRouter(prefix="/v1/academico")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/disciplinas/", response_model=list[DisciplinaOut])
def listar_disciplinas(db: Session = Depends(get_db)):
    return db.query(models.Disciplina).all()

@router.post("/disciplinas/", response_model=DisciplinaOut)
def criar_disciplina(payload: DisciplinaCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Disciplina).filter(models.Disciplina.nome == payload.nome).first()
    if exists:
        raise HTTPException(status_code=400, detail="Disciplina já existe")
    d = models.Disciplina(nome=payload.nome)
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.put("/disciplinas/{id}", response_model=DisciplinaOut)
def atualizar_disciplina(id: int, payload: DisciplinaCreate, db: Session = Depends(get_db)):
    d = db.query(models.Disciplina).get(id)
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    d.nome = payload.nome
    db.commit(); db.refresh(d)
    return d

@router.get("/assuntos/", response_model=list[AssuntoOut])
def listar_assuntos(disciplina_id: int = None, db: Session = Depends(get_db)):
    q = db.query(models.Assunto)
    if disciplina_id:
        q = q.filter(models.Assunto.disciplina_id == disciplina_id)
    return q.all()

@router.post("/assuntos/", response_model=AssuntoOut)
def criar_assunto(payload: AssuntoCreate, db: Session = Depends(get_db)):
    d = db.query(models.Disciplina).get(payload.disciplina_id)
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    a = models.Assunto(nome=payload.nome, disciplina_id=payload.disciplina_id)
    db.add(a); db.commit(); db.refresh(a)
    return a

@router.put("/assuntos/{id}", response_model=AssuntoOut)
def atualizar_assunto(id: int, payload: AssuntoCreate, db: Session = Depends(get_db)):
    a = db.query(models.Assunto).get(id)
    if not a:
        raise HTTPException(status_code=404, detail="Assunto não encontrado")
    a.nome = payload.nome
    a.disciplina_id = payload.disciplina_id
    db.commit(); db.refresh(a)
    return a

@router.get("/questoes/", response_model=list[QuestaoOut])
def listar_questoes(
    disciplina_id: int = None, assunto_id: int = None, dificuldade: int = None,
    tipo: str = None, db: Session = Depends(get_db)
):
    q = db.query(models.Questao)
    if disciplina_id:
        q = q.filter(models.Questao.disciplina_id == disciplina_id)
    if dificuldade:
        q = q.filter(models.Questao.dificuldade == dificuldade)
    if tipo:
        q = q.filter(models.Questao.tipo == tipo)
    if assunto_id:
        q = q.join(models.questao_assunto).filter(models.questao_assunto.c.assunto_id == assunto_id)
    return q.all()

@router.post("/questoes/", response_model=QuestaoOut)
def criar_questao(payload: QuestaoCreate, db: Session = Depends(get_db)):
    d = db.query(models.Disciplina).get(payload.disciplina_id)
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    assuntos = []
    for aid in payload.assuntos:
        a = db.query(models.Assunto).get(aid)
        if not a:
            raise HTTPException(status_code=404, detail=f"Assunto {aid} não encontrado")
        assuntos.append(a)

    nova = models.Questao(
        descricao=payload.descricao,
        dificuldade=payload.dificuldade,
        tipo=payload.tipo,
        disciplina_id=payload.disciplina_id,
    )
    nova.assuntos = assuntos
    db.add(nova); db.commit(); db.refresh(nova)
    return nova

@router.put("/questoes/{id}", response_model=QuestaoOut)
def atualizar_questao(id: int, payload: QuestaoCreate, db: Session = Depends(get_db)):
    qobj = db.query(models.Questao).get(id)
    if not qobj:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    d = db.query(models.Disciplina).get(payload.disciplina_id)
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    assuntos = []
    for aid in payload.assuntos:
        a = db.query(models.Assunto).get(aid)
        if not a:
            raise HTTPException(status_code=404, detail=f"Assunto {aid} não encontrado")
        assuntos.append(a)

    qobj.descricao = payload.descricao
    qobj.dificuldade = payload.dificuldade
    qobj.tipo = payload.tipo
    qobj.disciplina_id = payload.disciplina_id
    qobj.assuntos = assuntos
    db.commit(); db.refresh(qobj)
    return qobj
