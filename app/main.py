import time
from fastapi import FastAPI, Request
from app.routers import usuarios, espacios, reservas

app = FastAPI(title="API Reservas UCN", description="Cátedra 1 - IDWM")

@app.middleware("http")
async def measure_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(duration)
    return response

app.include_router(usuarios.router)
app.include_router(espacios.router)
app.include_router(reservas.router)

@app.get("/")
def health_check():
    return {"mensaje": "API de Reservas funcionando correctamente"}