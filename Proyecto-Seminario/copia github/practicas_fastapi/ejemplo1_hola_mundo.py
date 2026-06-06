from fastapi import FastAPI

app = FastAPI(title="API de FinTech Nova", version="1.0.0")

@app.get("/")
async def raiz():
    return {
        "mensaje": "Bienvenido a FinTech Nova API",
        "version": "1.0.0"
    }