from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class PacienteHanseniase(BaseModel):
    id: int
    nome: str
    idade: int
    municipio: str
    status_avaliacao: str
    data_diagnostico: str
    classificacao_operacional: str

class CasoHanseniase(BaseModel):
    id: int
    paciente_id: int
    tipo_avaliacao: str
    data_avaliacao: str
    resultado: str
    prioridade: str

# Dados mockados - depois substitua pelo banco de dados
pacientes_hanseniase = [
    {
        "id": 1,
        "nome": "Maria Silva",
        "idade": 45,
        "municipio": "São Paulo",
        "status_avaliacao": "Pendente",
        "data_diagnostico": "2024-01-15",
        "classificacao_operacional": "Multibacilar"
    },
    {
        "id": 2,
        "nome": "João Santos",
        "idade": 38,
        "municipio": "Rio de Janeiro",
        "status_avaliacao": "Concluída",
        "data_diagnostico": "2024-02-20",
        "classificacao_operacional": "Paucibacilar"
    }
]

casos_hanseniase = [
    {
        "id": 1,
        "paciente_id": 1,
        "tipo_avaliacao": "Estratificação de Risco",
        "data_avaliacao": "2024-03-20",
        "resultado": "Alto Risco",
        "prioridade": "Alta"
    },
    {
        "id": 2,
        "paciente_id": 2,
        "tipo_avaliacao": "Acompanhamento",
        "data_avaliacao": "2024-03-18",
        "resultado": "Baixo Risco",
        "prioridade": "Baixa"
    }
]

@router.get("/hanseniase/pacientes", response_model=List[PacienteHanseniase])
async def listar_pacientes():
    return pacientes_hanseniase

@router.get("/hanseniase/pacientes/{paciente_id}")
async def obter_paciente(paciente_id: int):
    paciente = next((p for p in pacientes_hanseniase if p["id"] == paciente_id), None)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@router.get("/hanseniase/casos", response_model=List[CasoHanseniase])
async def listar_casos():
    return casos_hanseniase

@router.get("/hanseniase/estatisticas")
async def obter_estatisticas():
    total_pacientes = len(pacientes_hanseniase)
    avaliacoes_pendentes = len([p for p in pacientes_hanseniase if p["status_avaliacao"] == "Pendente"])
    casos_alto_risco = len([c for c in casos_hanseniase if c["prioridade"] == "Alta"])
    
    return {
        "total_pacientes": total_pacientes,
        "avaliacoes_pendentes": avaliacoes_pendentes,
        "casos_alto_risco": casos_alto_risco,
        "casos_media_risco": len([c for c in casos_hanseniase if c["prioridade"] == "Média"]),
        "casos_baixo_risco": len([c for c in casos_hanseniase if c["prioridade"] == "Baixa"]),
        "taxa_avaliacao_pendente": (avaliacoes_pendentes / total_pacientes * 100) if total_pacientes > 0 else 0
    }