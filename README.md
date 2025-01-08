-- Introduccion: API  de Recomendacion de Peliculas. --
Desarrollada con FasAPI, IDE: Pycharm Professional, Asistente IA: ChatGPT Plus o1
Proporciona funcionalidades relacionadas con películas, incluyendo análisis, información y un sistema de recomendación basado en similitud.
Estructurada en base a datasets derivados de la ingesta y transformacion de los provistos en el repositorio. "peliculas_dataset_sumario.csv" fue obtenido a partir de "movies_dataset.csv"; mientras que "actores_desanidado.csv" y "directores_desanidado.csv" fueron derivados de "credits.csv".

-- Endpoints Disponibles:
1. / (Root)
Método: GET
Descripción: Endpoint de bienvenida.

2. /cantidad_filmaciones_mes/
Método: GET
Parámetros: mes (str): Nombre del mes en español.
Descripción: Devuelve la cantidad de películas estrenadas en un mes específico.

3. /cantidad_filmaciones_dia/
Método: GET
Parámetros: dia (str): Nombre del día en español.
Descripción: Devuelve la cantidad de películas estrenadas en un día específico de la semana.

4. /score_titulo/
Método: GET
Parámetros: titulo (str): Título de la película.
Descripción: Devuelve el score (puntuación) y año de estreno de una película.

5. /votos_titulo/
Método: GET
Parámetros: titulo (str): Título de la película.
Descripción: Devuelve el total de votos y promedio de puntuación para una película, si cumple con el mínimo de 2000 votos.

6. /get_actor/
Método: GET
Parámetros: nombre_actor (str): Nombre del actor.
Descripción: Descripción: Proporciona información sobre el éxito de un actor basado en las películas en las que ha participado, incluyendo el número total de películas, el retorno financiero acumulado, y el promedio por película. El retorno financiero acumulado se calcula sumando el valor de las columnas 'revenue' menos 'budget' para todas las películas en las que el actor ha participado. El promedio se obtiene dividiendo el retorno total entre la cantidad de películas en las que ha trabajado. También se listan las películas principales en las que ha trabajado.

7. /get_director/
Método: GET
Parámetros: nombre_director (str): Nombre del director.
Descripción: Proporciona el retorno financiero acumulado y detalles sobre las películas dirigidas por un director. El retorno financiero acumulado se calcula sumando el valor de las columnas 'revenue' menos 'budget' para todas las películas dirigidas por el director. También incluye detalles individuales de cada película, como el título, la fecha de lanzamiento, el retorno individual (revenue - budget), el costo (budget), y la ganancia neta (revenue - budget).

8. /recomendacion/
Método: GET
Parámetros: titulo (str): Título de la película.
            n_recomendaciones (int): Número de recomendaciones a devolver (por defecto 5).
Descripción: Este endpoint utiliza un sistema de recomendación basado en similitud para encontrar películas similares al título proporcionado. Internamente, compara características como géneros, puntuación promedio (vote_average) y popularidad (popularity). Se calcula la similitud del coseno entre las películas para determinar cuáles son las más cercanas.


-- Instalación y Ejecución Local --

1. Clonar el Repositorio

2. Instalar Dependencias

pip install -r requirements.txt

3. Ejecutar el Servidor

uvicorn main:app --reload

4. Acceder a la API

Documentación Swagger: http://127.0.0.1:8000/docs

Ejemplo de endpoint: http://127.0.0.1:8000/recomendacion/?titulo=Toy%20Story&n_recomendaciones=5

Despliegue en Render

La API está desplegada en Render y accesible en: https://fast-api-funcional.onrender.com/

