from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.esquemas import EspacioCreate, EspacioResponse
from app.repositories.repositorios import EspacioRepository
from app.services.servicios import EspacioService

router = APIRouter(prefix="/api/espacios", tags=["Espacios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_espacio_service(db: Session = Depends(get_db)):
    return EspacioService(EspacioRepository(db))

@router.get("", response_model=list[EspacioResponse])
def listar_espacios(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    capacidad: int | None = Query(default=None, gt=0),
    disponible: bool | None = Query(default=None),
    servicio: EspacioService = Depends(get_espacio_service)
):
    return servicio.get_all(page=page, limit=limit, capacidad=capacidad, disponible=disponible)

@router.get("/{id}", response_model=EspacioResponse)
def obtener_espacio(id: int, servicio: EspacioService = Depends(get_espacio_service)):
    return servicio.get_by_id(id)

@router.post("", response_model=EspacioResponse, status_code=status.HTTP_201_CREATED)
def crear_espacio(espacio: EspacioCreate, servicio: EspacioService = Depends(get_espacio_service)):
    return servicio.create(espacio)

@router.put("/{id}", response_model=EspacioResponse)
def actualizar_espacio(id: int, espacio: EspacioCreate, servicio: EspacioService = Depends(get_espacio_service)):
    return servicio.update(id, espacio)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_espacio(id: int, servicio: EspacioService = Depends(get_espacio_service)):
    return servicio.delete(id)