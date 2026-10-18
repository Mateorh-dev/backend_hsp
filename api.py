# endpoint de acceso
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.router import paciente, estadocita, cita, tratamiento, citaportratamiento
#imagen
import app.model.triggers

app = FastAPI()
api = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")  
async def Check(): 
    return {"mensaje": "Hola, este es el backend de HSP"}

api.include_router(paciente.router)
api.include_router(tratamiento.router)
api.include_router(citaportratamiento.router)
api.include_router(cita.router)
api.include_router(estadocita.router)
# api.include_router(imagen.router)

# app.include_router(general.router)
app.include_router(api)
