from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    reservas = relationship("Reserva", back_populates="usuario")

class Espacio(Base):
    __tablename__ = "espacios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    disponibilidad_total = Column(Boolean, default=True)
    
    reservas = relationship("Reserva", back_populates="espacio")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    espacio_id = Column(Integer, ForeignKey("espacios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String, default="activa")
    
    usuario = relationship("Usuario", back_populates="reservas")
    espacio = relationship("Espacio", back_populates="reservas")