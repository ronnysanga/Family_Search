from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health

app = FastAPI(
    title="Family Search API",
    description="API para el sistema de búsqueda de familiares",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza con los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router)

@app.get("/", tags=["Inicio"])
async def read_root():
    return {"mensaje": "Bienvenido a la API de Family Search"}