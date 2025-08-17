from fastapi import APIRouter, HTTPException
from config.database import test_connection

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
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
