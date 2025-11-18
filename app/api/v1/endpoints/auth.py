from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

fake_users_db = {
    "111.111.111-11": {
        "cpf": "111.111.111-11",
        "hashed_password": "$2b$12$0bK/JR.1pMv18sivgpOhVOUDMlepQ6kPv3G60ZCwcSf/O.ZMR9Ff.",
        "funcao": "medico",
        "full_name": "Dr. João da Silva",
        "disabled": False,
    },
    "222.222.222-22": {
        "cpf": "222.222.222-22",
        "hashed_password": "$2b$12$gifXAvouvlQwv24Z5QAPwOjgCTSjKPIQQKq.TuLsSRnHzD/xOhhCy",
        "funcao": "agente",
        "full_name": "Maria Agente",
        "disabled": False,
    },
    "333.333.333-33": {
        "cpf": "333.333.333-33",
        "hashed_password": "$2b$12$J/GXJQiXVMlvjWyw3H2kUu9lHffjFMehDy1Fb6Ivelwat56S1kdhO",
        "funcao": "enfermeiro",
        "full_name": "Enf. Carlos Pereira",
        "disabled": False,
    },
    "444.444.444-44": {
        "cpf": "444.444.444-44",
        "hashed_password": "$2b$12$pGog4eLuiRnh1jfuyeYb2u2/5tdxZhVNmbANHLQzAM934HPrgoKP6",
        "funcao": "administrador",
        "full_name": "Ana Administradora",
        "disabled": False,
    },
    "555.555.555-55": {
        "cpf": "555.555.555-55",
        "cns": "123456789012345",
        "hashed_password": "$2b$12$zDCWc5/c6y8dT1nI0KuQIeo4GWenzrVYRF1pB2VRMhhdHmQji5ERK",
        "funcao": "paciente",
        "full_name": "José Paciente",
        "disabled": False,
    }
}

def normalizar_cpf(cpf: str) -> str:
    """Remove máscara do CPF e formata para o padrão com máscara"""
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if len(cpf_limpo) == 11:
        # Formata para o padrão com máscara: 111.111.111-11
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cpf_normalizado = normalizar_cpf(form_data.username)
    
    print(f"🔍 DEBUG: CPF recebido: '{form_data.username}'")
    print(f"🔍 DEBUG: CPF normalizado: '{cpf_normalizado}'")
    print(f"🔍 DEBUG: Senha recebida: '{form_data.password}'")
    
    user_dict = fake_users_db.get(cpf_normalizado)
    print(f"🔍 DEBUG: Usuário encontrado: {user_dict is not None}")
    
    if not user_dict:
        print(f"❌ DEBUG: CPF '{cpf_normalizado}' não encontrado")
        print(f"🔍 DEBUG: CPFs disponíveis: {list(fake_users_db.keys())}")
        raise HTTPException(status_code=400, detail="CPF não encontrado")
    
    # Mapeamento de senhas
    senhas_corretas = {
        "111.111.111-11": "senha123",
        "222.222.222-22": "agente456",
        "333.333.333-33": "admin789",
        "444.444.444-44": "usuario000",
        "555.555.555-55": "paciente001"
    }
    
    senha_correta = senhas_corretas.get(cpf_normalizado)
    print(f"🔍 DEBUG: Senha esperada: '{senha_correta}'")
    
    if not senha_correta or form_data.password != senha_correta:
        print("❌ DEBUG: Senha incorreta")
        raise HTTPException(status_code=400, detail="Senha incorreta")
    
    print("✅ DEBUG: Login bem-sucedido!")
    return {
        "access_token": user_dict["cpf"],
        "token_type": "bearer",
        "user": {
            "cpf": user_dict["cpf"],
            "funcao": user_dict["funcao"],
            "full_name": user_dict["full_name"]
        }
    }

@router.get("/test")
async def test_endpoint():
    return {"message": "API de autenticação funcionando!"}
