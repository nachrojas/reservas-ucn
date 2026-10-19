import datetime
from app.database import SessionLocal
from app.models.modelos import Usuario, Espacio, Reserva

def cargar_datos():
    db = SessionLocal()
    try:
        # Validación para evitar datos duplicados si el script se ejecuta más de una vez
        if db.query(Usuario).first():
            print("Los datos iniciales ya fueron cargados previamente.")
            return

        # Carga de 5 usuarios requeridos
        usuarios = [
            Usuario(nombre="Ignacio Rojas", correo="ignacio@ucn.cl"),
            Usuario(nombre="Henry Maquera", correo="henry@ucn.cl"),
            Usuario(nombre="Pablo Salas", correo="pablo@ucn.cl"),
            Usuario(nombre="Fran", correo="fran@ucn.cl"),
            Usuario(nombre="José Benítez", correo="jose.benitez@ce.ucn.cl")
        ]
        db.add_all(usuarios)
        db.commit()

        # Carga de 10 espacios requeridos
        espacios = [
            Espacio(nombre=f"Laboratorio {i}", ubicacion="Pabellón K", capacidad=20, disponibilidad_total=True) for i in range(1, 11)
        ]
        db.add_all(espacios)
        db.commit()

        # Carga de 15 reservas requeridas
        reservas = []
        for i in range(1, 16):
            reservas.append(Reserva(
                usuario_id=(i % 5) + 1,
                espacio_id=(i % 10) + 1,
                fecha=datetime.date(2026, 10, 20),
                hora_inicio=datetime.time(8 + (i % 5), 0),
                hora_fin=datetime.time(9 + (i % 5), 0),
                estado="activa"
            ))
        db.add_all(reservas)
        db.commit()
        
        print("Se cargaron 5 usuarios, 10 espacios y 15 reservas con éxito.")
    finally:
        db.close()

if __name__ == "__main__":
    cargar_datos()