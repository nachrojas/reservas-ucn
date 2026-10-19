from abc import ABC, abstractmethod
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.modelos import Usuario, Espacio, Reserva
from app.schemas.esquemas import UsuarioCreate, EspacioCreate, ReservaCreate, ReservaUpdate

class IRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int):
        pass

class UsuarioRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        statement = select(Usuario).offset(skip).limit(limit)
        return self.db.execute(statement).scalars().all()

    def get_by_id(self, usuario_id: int):
        return self.db.get(Usuario, usuario_id)

    def get_by_correo(self, correo: str):
        statement = select(Usuario).where(Usuario.correo == correo)
        return self.db.execute(statement).scalars().first()

    def add(self, usuario: UsuarioCreate):
        db_usuario = Usuario(**usuario.model_dump())
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def update(self, db_usuario: Usuario, datos: UsuarioCreate):
        for key, value in datos.model_dump().items():
            setattr(db_usuario, key, value)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def delete(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()

class EspacioRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10, capacidad: int = None, disponible: bool = None):
        statement = select(Espacio)
        if capacidad is not None:
            statement = statement.where(Espacio.capacidad >= capacidad)
        if disponible is not None:
            statement = statement.where(Espacio.disponibilidad_total == disponible)
        statement = statement.offset(skip).limit(limit)
        return self.db.execute(statement).scalars().all()

    def get_by_id(self, espacio_id: int):
        return self.db.get(Espacio, espacio_id)

    def add(self, espacio: EspacioCreate):
        db_espacio = Espacio(**espacio.model_dump())
        self.db.add(db_espacio)
        self.db.commit()
        self.db.refresh(db_espacio)
        return db_espacio

    def update(self, db_espacio: Espacio, datos: EspacioCreate):
        for key, value in datos.model_dump().items():
            setattr(db_espacio, key, value)
        self.db.commit()
        self.db.refresh(db_espacio)
        return db_espacio

    def delete(self, espacio: Espacio):
        self.db.delete(espacio)
        self.db.commit()

class ReservaRepository(IRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        usuario_id: int = None,
        espacio_id: int = None,
        fecha: date = None,
        estado: str = None
    ):
        statement = select(Reserva)
        if usuario_id is not None:
            statement = statement.where(Reserva.usuario_id == usuario_id)
        if espacio_id is not None:
            statement = statement.where(Reserva.espacio_id == espacio_id)
        if fecha is not None:
            statement = statement.where(Reserva.fecha == fecha)
        if estado is not None:
            statement = statement.where(Reserva.estado == estado)
        statement = statement.offset(skip).limit(limit)
        return self.db.execute(statement).scalars().all()

    def get_by_id(self, reserva_id: int):
        return self.db.get(Reserva, reserva_id)

    def add(self, reserva: ReservaCreate):
        db_reserva = Reserva(**reserva.model_dump())
        self.db.add(db_reserva)
        self.db.commit()
        self.db.refresh(db_reserva)
        return db_reserva

    def update_partial(self, db_reserva: Reserva, datos: ReservaUpdate):
        # PATCH: Solo actualiza los campos que el cliente envió realmente
        campos_enviados = datos.model_dump(exclude_unset=True)
        for key, value in campos_enviados.items():
            setattr(db_reserva, key, value)
        self.db.commit()
        self.db.refresh(db_reserva)
        return db_reserva

    def delete(self, reserva: Reserva):
        self.db.delete(reserva)
        self.db.commit()