from datetime import date
from fastapi import HTTPException
from app.repositories.repositorios import UsuarioRepository, EspacioRepository, ReservaRepository
from app.schemas.esquemas import UsuarioCreate, EspacioCreate, ReservaCreate, ReservaUpdate

class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def get_all(self, page: int = 1, limit: int = 10):
        skip = (page - 1) * limit
        return self.repo.get_all(skip=skip, limit=limit)

    def get_by_id(self, usuario_id: int):
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    def create(self, usuario: UsuarioCreate):
        if self.repo.get_by_correo(usuario.correo):
            raise HTTPException(status_code=422, detail="El correo ya está registrado")
        return self.repo.add(usuario)

    def update(self, usuario_id: int, datos: UsuarioCreate):
        db_usuario = self.get_by_id(usuario_id)
        existente = self.repo.get_by_correo(datos.correo)
        if existente and existente.id != usuario_id:
            raise HTTPException(status_code=422, detail="El correo ya pertenece a otro usuario")
        return self.repo.update(db_usuario, datos)

    def delete(self, usuario_id: int):
        db_usuario = self.get_by_id(usuario_id)
        self.repo.delete(db_usuario)
        return {"mensaje": "Usuario eliminado correctamente"}

class EspacioService:
    def __init__(self, repo: EspacioRepository):
        self.repo = repo

    def get_all(self, page: int = 1, limit: int = 10, capacidad: int = None, disponible: bool = None):
        skip = (page - 1) * limit
        return self.repo.get_all(skip=skip, limit=limit, capacidad=capacidad, disponible=disponible)

    def get_by_id(self, espacio_id: int):
        espacio = self.repo.get_by_id(espacio_id)
        if not espacio:
            raise HTTPException(status_code=404, detail="Espacio no encontrado")
        return espacio

    def create(self, espacio: EspacioCreate):
        return self.repo.add(espacio)

    def update(self, espacio_id: int, datos: EspacioCreate):
        db_espacio = self.get_by_id(espacio_id)
        return self.repo.update(db_espacio, datos)

    def delete(self, espacio_id: int):
        db_espacio = self.get_by_id(espacio_id)
        self.repo.delete(db_espacio)
        return {"mensaje": "Espacio eliminado correctamente"}

class ReservaService:
    def __init__(self, repo: ReservaRepository, espacio_repo: EspacioRepository, usuario_repo: UsuarioRepository):
        self.repo = repo
        self.espacio_repo = espacio_repo
        self.usuario_repo = usuario_repo

    def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        usuario_id: int = None,
        espacio_id: int = None,
        fecha: date = None,
        estado: str = None
    ):
        skip = (page - 1) * limit
        return self.repo.get_all(
            skip=skip, limit=limit, usuario_id=usuario_id, espacio_id=espacio_id, fecha=fecha, estado=estado
        )

    def get_by_id(self, reserva_id: int):
        reserva = self.repo.get_by_id(reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva

    def _validar_horario_y_superposicion(self, espacio_id: int, fecha, hora_inicio, hora_fin, excluir_id: int = None):
        if hora_inicio >= hora_fin:
            raise HTTPException(status_code=422, detail="Horario no válido: La hora de inicio debe ser menor a la hora de fin.")

        reservas_existentes = self.repo.get_all(espacio_id=espacio_id, fecha=fecha, limit=1000)
        for r in reservas_existentes:
            if excluir_id is not None and r.id == excluir_id:
                continue
            if r.estado != "cancelada":
                if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                    raise HTTPException(
                        status_code=422,
                        detail="Reserva duplicada: El espacio ya está reservado en un horario que se superpone."
                    )

    def create(self, reserva: ReservaCreate):
        if not self.usuario_repo.get_by_id(reserva.usuario_id):
            raise HTTPException(status_code=404, detail="Usuario inexistente")
        espacio = self.espacio_repo.get_by_id(reserva.espacio_id)
        if not espacio:
            raise HTTPException(status_code=404, detail="Espacio inexistente")
        if not espacio.disponibilidad_total:
            raise HTTPException(status_code=422, detail="El espacio no se encuentra disponible para reservas")

        self._validar_horario_y_superposicion(reserva.espacio_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin)
        return self.repo.add(reserva)

    def patch(self, reserva_id: int, datos: ReservaUpdate):
        db_reserva = self.get_by_id(reserva_id)
        
        nuevo_usuario_id = datos.usuario_id if datos.usuario_id is not None else db_reserva.usuario_id
        nuevo_espacio_id = datos.espacio_id if datos.espacio_id is not None else db_reserva.espacio_id
        nueva_fecha = datos.fecha if datos.fecha is not None else db_reserva.fecha
        nueva_hora_inicio = datos.hora_inicio if datos.hora_inicio is not None else db_reserva.hora_inicio
        nueva_hora_fin = datos.hora_fin if datos.hora_fin is not None else db_reserva.hora_fin
        nuevo_estado = datos.estado if datos.estado is not None else db_reserva.estado

        if not self.usuario_repo.get_by_id(nuevo_usuario_id):
            raise HTTPException(status_code=404, detail="Usuario inexistente")
        if not self.espacio_repo.get_by_id(nuevo_espacio_id):
            raise HTTPException(status_code=404, detail="Espacio inexistente")

        if nuevo_estado != "cancelada":
            self._validar_horario_y_superposicion(
                nuevo_espacio_id, nueva_fecha, nueva_hora_inicio, nueva_hora_fin, excluir_id=reserva_id
            )

        return self.repo.update_partial(db_reserva, datos)

    def delete(self, reserva_id: int):
        reserva = self.get_by_id(reserva_id)
        self.repo.delete(reserva)
        return {"mensaje": "Reserva eliminada correctamente"}