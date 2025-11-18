from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class ContatoTuberculose(BaseModel):
    id: int
    nome: str
    idade: int
    municipio: str
    tipo_contato: str
    status_convocação: str
    data_ultimo_contato: str

class TratamentoTuberculose(BaseModel):
    id: int
    paciente_id: int
    tipo_tratamento: str
    data_inicio: str
    data_termino: str
    status: str

# Dados mockados
contatos_tuberculose = [
    {
        "id": 1,
        "nome": "Ana Oliveira",
        "idade": 32,
        "municipio": "Rio de Janeiro",
        "tipo_contato": "Domiciliar",
        "status_convocação": "Pendente",
        "data_ultimo_contato": "2024-03-18"
    },
    {
        "id": 2,
        "nome": "Carlos Mendes",
        "idade": 28,
        "municipio": "São Paulo",
        "tipo_contato": "Laboral",
        "status_convocação": "Convocado",
        "data_ultimo_contato": "2024-03-15"
    }
]

tratamentos_tuberculose = [
    {
        "id": 1,
        "paciente_id": 1,
        "tipo_tratamento": "TPT",
        "data_inicio": "2024-03-20",
        "data_termino": "2024-09-20",
        "status": "Em andamento"
    },
    {
        "id": 2,
        "paciente_id": 2,
        "tipo_tratamento": "TPT",
        "data_inicio": "2024-02-15",
        "data_termino": "2024-08-15",
        "status": "Concluído"
    }
]

@router.get("/tuberculose/contatos", response_model=List[ContatoTuberculose])
async def listar_contatos():
    return contatos_tuberculose

@router.get("/tuberculose/contatos/{contato_id}")
async def obter_contato(contato_id: int):
    contato = next((c for c in contatos_tuberculose if c["id"] == contato_id), None)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contato

@router.get("/tuberculose/tratamentos", response_model=List[TratamentoTuberculose])
async def listar_tratamentos():
    return tratamentos_tuberculose

@router.get("/tuberculose/estatisticas")
async def obter_estatisticas():
    total_contatos = len(contatos_tuberculose)
    contatos_pendentes = len([c for c in contatos_tuberculose if c["status_convocação"] == "Pendente"])
    tpt_andamento = len([t for t in tratamentos_tuberculose if t["status"] == "Em andamento"])
    
    return {
        "total_contatos": total_contatos,
        "contatos_pendentes": contatos_pendentes,
        "tpt_andamento": tpt_andamento,
        "tpt_concluido": len([t for t in tratamentos_tuberculose if t["status"] == "Concluído"]),
        "taxa_convocação_pendente": (contatos_pendentes / total_contatos * 100) if total_contatos > 0 else 0
    }