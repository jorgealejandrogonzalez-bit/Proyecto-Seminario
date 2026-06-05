from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(title="API de Predicción de Datos", version="1.0")

# --- NUEVO: Inicializar el esquema de seguridad para Hardening ---
security = HTTPBasic()

# Base de datos simulada
datos_usuarios = {"user1": "Activo", "user2": "Inactivo"}

# --- NUEVO: Credenciales válidas para el Administrador de Seguridad ---
USUARIO_ADMIN = "admin"
PASSWORD_ADMIN = "supersecret123"

# --- NUEVO: Función verificadora que obligará a retornar el error 401 ---
def verificar_autenticacion(credentials: HTTPBasicCredentials = Depends(security)):
    """Valida que el usuario esté autenticado para proteger la información confidencial"""
    if credentials.username != USUARIO_ADMIN or credentials.password != PASSWORD_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado: Credenciales inválidas o ausentes",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}

@app.get("/status")
def health_check():
    return {"status": "ok", "servicios": "operativos"}

# --- MODIFICADO: Endpoint protegido con la dependencia de seguridad ---
@app.get("/datos-sensibles/{usuario}")
def obtener_datos_privados(usuario: str, admin_user: str = Depends(verificar_autenticacion)):
    if usuario in datos_usuarios:
        return {
            "usuario": usuario, 
            "estado": datos_usuarios[usuario], 
            "datos_financieros": "Confidencial",
            "auditoria": f"Acceso protegido concedido a: {admin_user}"
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")