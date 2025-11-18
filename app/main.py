from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import auth, hanseniase, tuberculose
import os

app = FastAPI(title="Monitora SUS API")

# ================================================================
# ✅ CONFIGURAÇÃO DE CORS (Frontend React/Vite acessando via IP)
# ================================================================
# Caso o IP da sua máquina mude com frequência, use allow_origin_regex
# para permitir qualquer IP da sua rede local (192.168.*.*:5173)
# ou comente a linha da regex e use apenas allow_origins fixos.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # acesso local
        "http://127.0.0.1:5173",       # acesso via loopback
        "http://192.168.18.10:5173",   # acesso pelo IP do notebook (para celular)
    ],
    allow_origin_regex=r"^http://192\.168\.\d{1,3}\.\d{1,3}:5173$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================================
# 📂 CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS
# ================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
static_files_path = os.path.join(project_root, "static")

print(f"🔍 DEBUG: Procurando static em: {static_files_path}")

if not os.path.exists(static_files_path):
    print("📁 Criando pasta static...")
    os.makedirs(static_files_path)

app.mount("/static", StaticFiles(directory=static_files_path), name="static")

# ================================================================
# 🔗 ROTAS
# ================================================================
# Autenticação
app.include_router(auth.router, prefix="/api/v1/token", tags=["Authentication"])

# Hanseníase
app.include_router(hanseniase.router, prefix="/api/v1", tags=["Hanseníase"])

# Tuberculose
app.include_router(tuberculose.router, prefix="/api/v1", tags=["Tuberculose"])

# ================================================================
# 🏠 ROTA PRINCIPAL / TESTE DE SAÚDE
# ================================================================
@app.get("/")
async def read_index():
    index_path = os.path.join(static_files_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {"message": "Backend funcionando! Acesse /docs para documentação."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}
