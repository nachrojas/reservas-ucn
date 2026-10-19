from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.esquemas import ReservaCreate, ReservaUpdate, ReservaResponse
from app.repositories.repositorios import ReservaRepository, EspacioRepository, UsuarioRepository
from app.services.servicios import ReservaService

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reserva_service(db: Session = Depends(get_db)):
    return ReservaService(
        ReservaRepository(db),
        EspacioRepository(db),
        UsuarioRepository(db)
    )

@router.get("", response_model=list[ReservaResponse])
def listar_reservas(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    usuario: int | None = Query(default=None),
    espacio: int | None = Query(default=None),
    fecha: date | None = Query(default=None),
    estado: str | None = Query(default=None),
    servicio: ReservaService = Depends(get_reserva_service)
):
    return servicio.get_all(
        page=page, limit=limit, usuario_id=usuario, espacio_id=espacio, fecha=fecha, estado=estado
    )

@router.get("/{id}", response_model=ReservaResponse)
def obtener_reserva(id: int, servicio: ReservaService = Depends(get_reserva_service)):
    return servicio.get_by_id(id)

@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: ReservaCreate, servicio: ReservaService = Depends(get_reserva_service)):
    return servicio.create(reserva)

@router.patch("/{id}", response_model=ReservaResponse)
def actualizar_parcial_reserva(id: int, reserva: ReservaUpdate, servicio: ReservaService = Depends(get_reserva_service)):
    return servicio.patch(id, reserva)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_reserva(id: int, servicio: ReservaService = Depends(get_reserva_service)):
    return servicio.delete(id)