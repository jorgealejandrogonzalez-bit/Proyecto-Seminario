import sqlite3
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="FinTech Nova - Secure API Practice")

# MIDDLEWARE DE CABECERAS DE SEGURIDAD CORREGIDO
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # CSP Corregido: Permite cargar los estilos y scripts que FastAPI/Swagger trae desde CDN de forma segura
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https://fastapi.tiangolo.com;"
    )
    return response


# 2. BASE DE DATOS EN MEMORIA COMPARTIDA
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)"
    )
    cursor.execute("DELETE FROM users")
    cursor.executemany(
        "INSERT INTO users (username, role) VALUES (?, ?)",
        [("admin", "superadmin"), ("juan", "user"), ("maria", "user")],
    )
    conn.commit()
    return conn

db_conn = init_db()


# 3. RUTA VULNERABLE (Línea donde fallaba la indentación)
@app.get("/vulnerable/users/{username}")
def get_user_vulnerable(username: str):
    cursor = db_conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return {"query_ejecutada": query, "resultado": result}
    except Exception as e:
        return {"error": str(e)}


# 4. RUTA SEGURA
@app.get("/secure/users/{username}")
def get_user_secure(username: str):
    cursor = db_conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    return {"query_ejecutada": query, "resultado": result}