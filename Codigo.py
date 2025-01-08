import pandas as pd
import json
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ------------------------
# Carga y Preprocesamiento
# ------------------------

# Carga de datasets
df = pd.read_csv("Datasets/peliculas_dataset_sumario.csv", low_memory=False)
movies_df = pd.read_csv("Datasets/peliculas_dataset_sumario.csv", low_memory=False)
cast_df = pd.read_csv("Datasets/actores_desanidado.csv")
directores_df = pd.read_csv("Datasets/directores_desanidado.csv", low_memory=False)

# Convertir la columna 'release_date' a datetime
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Extraer géneros
def extraer_generos(genre_str):
    try:
        generos = json.loads(genre_str.replace("'", "\""))
        return [g['name'] for g in generos]
    except:
        return []

movies_df['genres_list'] = movies_df['genres'].apply(extraer_generos)

# -----------------
# Funciones de EDA
# -----------------

# Diccionario para meses en español
meses_espanol = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

def cantidad_filmaciones_mes(mes: str) -> str:
    mes = mes.lower()
    if mes not in meses_espanol:
        return "Mes ingresado no válido."
    numero_mes = meses_espanol[mes]
    filmaciones_en_mes = df[df["release_date"].dt.month == numero_mes]
    cantidad = filmaciones_en_mes.shape[0]
    return f"{cantidad} películas fueron estrenadas en {mes.capitalize()}."

# Diccionario para días en español
dias_espanol = {
    'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
    'viernes': 4, 'sábado': 5, 'domingo': 6
}

def cantidad_filmaciones_dia(dia: str) -> str:
    dia = dia.lower()
    if dia not in dias_espanol:
        return "Día ingresado no válido."
    numero_dia = dias_espanol[dia]
    df_valid = df.dropna(subset=['release_date'])
    filmaciones_en_dia = df_valid[df_valid['release_date'].dt.weekday == numero_dia]
    cantidad = filmaciones_en_dia.shape[0]
    return f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}."

# ---------------------------
# Funciones de Información
# ---------------------------

def score_titulo(titulo: str) -> str:
    titulo = df[df['title'].str.lower() == titulo.lower()]
    if titulo.empty:
        return "No se encontró ninguna filmación con ese título."
    resultado = titulo.iloc[0]
    año_estreno = resultado['release_date'].year if pd.notnull(resultado['release_date']) else "No disponible"
    score = resultado['vote_average'] if 'vote_average' in resultado else "No disponible"
    return f"La película '{resultado['title']}' fue estrenada en {año_estreno} con un score de {score}."

def votos_titulo(titulo: str) -> str:
    titulo = df[df['title'].str.lower() == titulo.lower()]
    if titulo.empty:
        return "No se encontró ninguna filmación con ese título."
    resultado = titulo.iloc[0]
    if resultado['vote_count'] < 2000:
        return f"La película '{resultado['title']}' no cumple con el mínimo de 2000 votos."
    cantidad_votos = int(resultado['vote_count'])
    promedio_votos = resultado['vote_average']
    año_estreno = resultado['release_date'].year if pd.notnull(resultado['release_date']) else "No disponible"
    return (
        f"La película '{resultado['title']}' fue estrenada en {año_estreno}. "
        f"Tiene {cantidad_votos} votos con un promedio de {promedio_votos}."
    )

def get_actor(nombre_actor: str) -> str:
    peliculas_actor = cast_df[cast_df['actor_name'].str.lower() == nombre_actor.lower()]
    if peliculas_actor.empty:
        return f"No se encontraron participaciones para el actor {nombre_actor}."
    peliculas_actor = peliculas_actor.merge(movies_df, left_on='movie_id', right_on='id', how='inner')
    peliculas_actor['return'] = peliculas_actor['return'].fillna(0)
    cantidad_peliculas = peliculas_actor.shape[0]
    retorno_total = peliculas_actor['return'].sum()
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    return (
        f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas, "
        f"con un retorno total de {retorno_total:.2f} y un promedio de {promedio_retorno:.2f}."
    )

def get_director(nombre_director: str) -> str:
    peliculas_director = directores_df[
        (directores_df['crew_name'].str.lower() == nombre_director.lower()) &
        (directores_df['job'] == 'Director')
    ]
    if peliculas_director.empty:
        return f"No se encontraron películas para el director {nombre_director}."
    peliculas_director = peliculas_director.merge(movies_df, left_on='movie_id', right_on='id', how='inner')
    peliculas_director['return'] = peliculas_director['return'].fillna(0)
    peliculas_director['budget'] = peliculas_director['budget'].fillna(0)
    peliculas_director['revenue'] = peliculas_director['revenue'].fillna(0)
    retorno_total = peliculas_director['return'].sum()
    detalle_peliculas = [
        f"Película: {row['title']}, Fecha: {row['release_date']}, Retorno: {row['return']:.2f}, "
        f"Costo: ${row['budget']:,.2f}, Ganancia: ${row['revenue'] - row['budget']:,.2f}"
        for _, row in peliculas_director.iterrows()
    ]
    return (
        f"El director {nombre_director} tiene un retorno total de {retorno_total:.2f}.\n"
        f"Detalle de sus películas:\n" + "\n".join(detalle_peliculas)
    )

# ---------------------------
# Funciones de Recomendación
# ---------------------------

def preprocesar_datos():
    mlb = MultiLabelBinarizer()
    generos_binarios = mlb.fit_transform(movies_df['genres_list'])
    scaler = MinMaxScaler()
    caracteristicas_numericas = scaler.fit_transform(movies_df[['vote_average', 'popularity']])
    return np.hstack([generos_binarios, caracteristicas_numericas])

def recomendacion_ml(titulo: str, n_recomendaciones: int = 5) -> list:
    vectores = preprocesar_datos()
    if titulo.lower() not in movies_df['title'].str.lower().values:
        return [f"No se encontró la película '{titulo}'."]
    indice_pelicula = movies_df[movies_df['title'].str.lower() == titulo.lower()].index[0]
    similitudes = cosine_similarity([vectores[indice_pelicula]], vectores).flatten()
    indices_similares = np.argsort(similitudes)[::-1][1:n_recomendaciones + 1]
    recomendaciones = movies_df.iloc[indices_similares]['title'].tolist()
    return recomendaciones

# Ejemplo de recomendación
resultado = recomendacion_ml("toy story", n_recomendaciones=5)
print("Recomendaciones:", resultado)
