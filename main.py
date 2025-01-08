from fastapi import FastAPI
from typing import List
from Codigo import (
    cantidad_filmaciones_mes,
    cantidad_filmaciones_dia,
    score_titulo,
    votos_titulo,
    get_actor,
    get_director,
    recomendacion_ml
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de películas"}

@app.get("/cantidad_filmaciones_mes/")
def api_cantidad_filmaciones_mes(mes: str):
    return {"result": cantidad_filmaciones_mes(mes)}

@app.get("/cantidad_filmaciones_dia/")
def api_cantidad_filmaciones_dia(dia: str):
    return {"result": cantidad_filmaciones_dia(dia)}

@app.get("/score_titulo/")
def api_score_titulo(titulo: str):
    return {"result": score_titulo(titulo)}

@app.get("/votos_titulo/")
def api_votos_titulo(titulo: str):
    return {"result": votos_titulo(titulo)}

@app.get("/get_actor/")
def api_get_actor(nombre_actor: str):
    return {"result": get_actor(nombre_actor)}

@app.get("/get_director/")
def api_get_director(nombre_director: str):
    return {"result": get_director(nombre_director)}

@app.get("/recomendacion/")
def api_recomendacion_ml(titulo: str, n_recomendaciones: int = 5):
    return {"recomendaciones": recomendacion_ml(titulo, n_recomendaciones)}
