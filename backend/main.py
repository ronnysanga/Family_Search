from fastapi import FastAPI, HTTPException
from config.database import test_connection

app = FastAPI(
    title="Family Search API",
    description="API para el sistema de búsqueda de familiares",
    version="1.0.0"
)

@app.get("/", tags=["Inicio"])
async def read_root():
    return {"mensaje": "Bienvenido a la API de Family Search"}

@app.get("/health", tags=["Salud"])
async def health_check():
    """
    Verifica el estado de salud de la API y la conexión a la base de datos.
    """
    try:
        # Probar conexión a la base de datos
        db_status = test_connection()
        if db_status["status"] == "success":
            return {
                "status": "ok",
                "database": db_status["database"],
                "message": "API y base de datos funcionando correctamente"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=db_status["message"]
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar el estado de la base de datos: {str(e)}"
        )