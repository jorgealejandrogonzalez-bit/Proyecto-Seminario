from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# --- MODIFICADO: Definir la función de verificación PRIMERO ---
# Credenciales válidas para el Administrador de Seguridad
USUARIO_ADMIN = "admin"
PASSWORD_ADMIN = "123456"

# Inicializar el esquema de seguridad para Hardening
security = HTTPBasic()

def verificar_autenticacion(credentials: HTTPBasicCredentials = Depends(security)):
    """Valida globalmente las credenciales antes de dar acceso a cualquier parte de la API"""
    if credentials.username != USUARIO_ADMIN or credentials.password != PASSWORD_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado: Credenciales inválidas o ausentes",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- MODIFICADO: Aplicar 'dependencies=[Depends(verificar_autenticacion)]' a nivel global ---
# Esto obliga a que LO PRIMERO que pida la API al cargar sea el usuario y contraseña.
app = FastAPI(
    title="API de Predicción de Datos", 
    version="1.0",
    dependencies=[Depends(verificar_autenticacion)]
)

# Base de datos simulada
datos_usuarios = {"user1": "Activo", "user2": "Inactivo"}

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}

@app.get("/status")
def health_check():
    return {"status": "ok", "servicios": "operativos"}

@app.get("/datos-sensibles/{usuario}")
def obtener_datos_privados(usuario: str):
    if usuario in datos_usuarios:
        return {
            "usuario": usuario, 
            "estado": datos_usuarios[usuario], 
            "datos_financieros": "Confidencial"
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")