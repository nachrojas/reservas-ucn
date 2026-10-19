from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.esquemas import UsuarioCreate, UsuarioResponse
from app.repositories.repositorios import UsuarioRepository
from app.services.servicios import UsuarioService

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_usuario_service(db: Session = Depends(get_db)):
    return UsuarioService(UsuarioRepository(db))

@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    servicio: UsuarioService = Depends(get_usuario_service)
):
    return servicio.get_all(page=page, limit=limit)

@router.get("/{id}", response_model=UsuarioResponse)
def obtener_usuario(id: int, servicio: UsuarioService = Depends(get_usuario_service)):
    return servicio.get_by_id(id)

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, servicio: UsuarioService = Depends(get_usuario_service)):
    return servicio.create(usuario)

@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: int, usuario: UsuarioCreate, servicio: UsuarioService = Depends(get_usuario_service)):
    return servicio.update(id, usuario)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(id: int, servicio: UsuarioService = Depends(get_usuario_service)):
    return servicio.delete(id)