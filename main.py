# Importaciones
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
import importlib
import pandas as pd
import operator
from fastapi.responses import JSONResponse

# Se instancia la aplicación
app = FastAPI()

# Se cargan los datos parquet en un dataframe de pandas
df_reviews_as = pd.read_parquet('DATA/df_developer_sanalysis.parquet')
df_games = pd.read_parquet('DATA/df_genres_year_1.parquet')
df_games_item = pd.read_parquet('DATA/genre_use_year_2.parquet')
df_games_title = pd.read_parquet('DATA/year_title_3.parquet')
df_developers = pd.read_parquet('DATA/year_developer_4.parquet')
df_modelo = pd.read_parquet('DATA/modelo_rec.parquet')
df_modelo_u=pd.read_parquet('DATA/modelo_rec_u.parquet')


#-------------------------------FUNCIONES------------------------------#

@app.get(path="/", response_class=HTMLResponse, tags=["Bienvenidos"])
def home():
    # Define el mensaje con HTML, incluyendo la imagen
    return '''  
      <html>
        <head>
            <title>PROYECTO INDIVIDUAL Nº1 - MLOps</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f0f0f0;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                h2 {
                    color: #555;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
                img {
                    display: block;
                    margin: 0 auto;
                    margin-top: 20px;
                    max-width: 100%;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <h1>PROYECTO INDIVIDUAL Nº1</h1>
            <h2>Machine Learning Operations (MLOps)</h2>
            <p>Nombre: MARTINEZ HERRERO MARIA GABRIELA</p>
            <p>Cohorte: DATA-FT17-G06</p>
            <!-- Reemplaza URL_DE_LA_IMAGEN con la URL real de la imagen -->
            <<img decoding="async" width="400" height="156" src="https://neurona-ba.com/wp-content/uploads/2021/07/HenryLogo.jpg" alt="Henry Logo" class="wp-image-5334" srcset="https://neurona-ba.com/wp-content/uploads/2021/07/HenryLogo.jpg 400w, https://neurona-ba.com/wp-content/uploads/2021/07/HenryLogo-300x117.jpg 300w" sizes="(max-width: 400px) 100vw, 400px">>
            <p>Escriba <span style="background-color: lightgray;">/docs</span> a continuación de la URL actual de esta página para interactuar con la API</p>
        </body>
    </html>
'''

#1)---------------------año con mas horas jugadas para dicho género---------------#
@app.get(path='/PlayTimeGenre',           
         description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero en el box inferior. Ejemplo de generos: Action (Casual, Indie, Simulation, etc)<br>
                        3. Scrollear a "Resposes"  para devolver año con más horas jugadas para dicho género. 
                        </font>
                        """,
         tags=["Consultas Generales"])
def PlayTimeGenre(genero: str):
    # Verificar si el género está en la base de datos
    if genero not in df_games['genres'].unique():
        raise HTTPException(status_code=400, detail=f"Error: El género '{genero}' no es válido.")

    # Filtrar el DataFrame por el género proporcionado
    genre_df = df_games[df_games['genres'] == genero]

    # Verificar si hay datos para el género seleccionado
    if genre_df.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para el género '{genero}' en la base de datos.")

    # Encontrar el año con más horas jugadas
    max_year = genre_df['release_year'].max()

    # Retornar los valores solicitados
    return {"Año de lanzamiento con más horas jugadas para Género {}: {}".format(genero, max_year)}

    
#2)-------------------usuario más horas jugadas para el género por año------------#

@app.get('/UserForGenre', 
         description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero en el box inferior. Ejemplo de generos: Action (Casual, Indie, Simulation, etc)<br>
                        3. Scrollear a "Resposes"  Usuario con más horas jugadas para el genero dado y descripción por año. 
                        </font>
                        """,
         tags=["Consultas Generales"])
def UserForGenre(genero: str):
    # Verificar si el género está en la base de datos
    if genero not in df_games_item['genres'].unique():
        raise HTTPException(status_code=400, detail=f"Error: El género '{genero}' no es válido.")

    # Filtrar por el género especificado
    df_genre = df_games_item[df_games_item['genres'] == genero]

    # Verificar si hay datos para el género seleccionado
    if df_genre.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para el género '{genero}' en la base de datos.")

    # Agrupar por usuario y género y calcular las horas jugadas sumando los valores
    df_genre_g = df_genre.groupby(['user_id'])['playtime_forever'].sum()

    # Encontrar el usuario con más horas jugadas
    max_playtime = df_genre_g.idxmax()

    # Agrupar por año y calcular las horas jugadas sumando los valores
    grouped_by_year = df_genre.groupby('release_year')['playtime_forever'].sum()

    # Crear lista de acumulación de horas jugadas por año
    horas_acum = [{'Año': year, 'Horas': hours} for year, hours in grouped_by_year.items()]

    # Retornar el resultado como un diccionario
    return {"Usuario con más horas jugadas para Género {}".format(genero): max_playtime, "Horas jugadas": horas_acum}     

#3)--------------3 de juegos MÁS recomendados por usuarios ----------------------#
@app.get('/UsersRecommend')
def UsersRecommend(año: int):
    # Verificar si el año proporcionado es válido
    if año not in df_games_title['release_year'].unique():
        raise HTTPException(status_code=404, detail=f"El año {año} no existe en los datos.")

    # Filtrar el DataFrame df_top3 por el año proporcionado
    top3_by_year = df_games_title[df_games_title['release_year'] == año]
    
    # Crear la lista de diccionarios
    resultado = []
    for index, row in top3_by_year.iterrows():
        puesto = row['rank']
        titulo = row['title']
        año = int(row['release_year'])
        resultado.append({f"Puesto {puesto}": f"{titulo}"})
    return resultado   
#4)------------------- top 3 de desarrolladoras con juegos MENOS recomendados-----------#

@app.get('/UsersWorstDeveloper', 
         description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el año en el box inferior. Ejemplo de año: 2011 (solo existen del 2011-2015)<br>
                        3. Scrollear a "Resposes"  top 3 de desarrolladoras con juegos MENOS recomendados
                        </font>
                        """,
         tags=["Consultas Generales"])
def UsersWorstDeveloper(año: int):
    # Verificar si el año está en el rango permitido
    años_permitidos = [2011, 2012, 2013, 2014, 2015]
    if año not in años_permitidos:
        raise HTTPException(status_code=400, detail=f"Error: El año '{año}' no es válido. Solo se permiten años en el rango 2011-2015.")

    # Filtrar el DataFrame df_developer por el año proporcionado
    developer_by_year = df_developers[df_developers['year'] == año]

    # Verificar si hay datos para el año seleccionado
    if developer_by_year.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para el año '{año}' en la base de datos.")

    # Obtener el top 3 de desarrolladoras con juegos MENOS recomendados y sus valores según rank
    top3_worst_developer = developer_by_year.sort_values(by='rank', ascending=False).head(3)

    # Formatear el resultado como lista de diccionarios
    result = [{"Puesto {}: {}".format(rank, developer)} for rank, developer in zip(top3_worst_developer['rank'], top3_worst_developer['developer'])]

    return result

#----------------------Analisis de Sentimiento----------------------------------#

@app.get('/sentiment_analysis',
         description=""" 
                    INSTRUCCIONES<br>
                    1. Para empezar haga click en -> "Try it out".<br>
                    2. Ingrese el nombre de empresa desarrolladora el en el box inferior.Ejemplo: tobyfox (11 bit studios, 07th Expansion,etc)<br>
                    3. Click a "Execute" listar por sentimiento las reseñas
                                      """,
         tags=["Analisis de Sentimiento"])
def sentiment_analysis(empresa_desarrolladora: str): 
    # Verificar si la empresa desarrolladora está en la base de datos
    if empresa_desarrolladora not in df_reviews_as['developer'].unique():
        raise HTTPException(status_code=400, detail=f"Error: La empresa desarrolladora '{empresa_desarrolladora}' no es válida.")

    # Filtrar el DataFrame por la empresa desarrolladora proporcionada
    developer_df = df_reviews_as[df_reviews_as['developer'] == empresa_desarrolladora]

    # Verificar si hay datos para la empresa desarrolladora seleccionada
    if developer_df.empty:
        raise HTTPException(status_code=404, detail=f"No hay datos para la empresa desarrolladora '{empresa_desarrolladora}' en la base de datos.")

    # Crear el diccionario de retorno
    result = {empresa_desarrolladora: {'Negative': 0, 'Neutral': 0, 'Positive': 0}}

    # Llenar el diccionario con la cantidad de registros para cada categoría de sentimiento
    for sentiment, count in zip(developer_df['sentiment_analysis'], developer_df['recommend_count']):
        sentiment_mapping = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        sentiment_category = sentiment_mapping[sentiment]
        result[empresa_desarrolladora][sentiment_category] += count

    return result


#6)------------------------------- item-item-----------------------------------------#

@app.get('/recomendacion_juego',
         description=""" 
                    INSTRUCCIONES<br>
                    1. Para empezar haga click en -> "Try it out".<br>
                    2. Ingrese el ID del juego en el recuadro inferior. Ejemplo de ID: 449940 (610660, 761140, etc)<br>
                    3. Click a "Execute" para juegos recomendados.
                    """,
         tags=["Recomendación"])
def recomendacion_juego(id_producto: int):
    # Verificar si el ID del juego está en la base de datos
    if id_producto not in df_modelo['item_id'].unique():
        raise HTTPException(status_code=400, detail=f"Error: El ID del juego '{id_producto}' no es válido o no se encuentra en la base de datos.")

    # Obtener las recomendaciones para el ID proporcionado
    recomendaciones = df_modelo[df_modelo['item_id'] == id_producto]['recomendaciones'].iloc[0]
    
    # Verificar si la lista de recomendaciones no está vacía
    if len(recomendaciones) > 0:
        recomendaciones_dict = {i + 1: juego for i, juego in enumerate(recomendaciones)}
        return recomendaciones_dict
    else:
        # Si no se encontraron recomendaciones para el ID, devolver un mensaje de error
        raise HTTPException(status_code=404, detail=f"No se encontraron recomendaciones para el ID del juego '{id_producto}'.")
#7)-----------------------------user-item-------------------------------------------#

@app.get('/recomendacion_juego_usuario', description=""" 
                    INSTRUCCIONES<br>
                    1. Para empezar haga click en -> "Try it out".<br>
                    2. Ingrese el ID del usuario en el recuadro inferior. Ejemplo de UD_USIARIO: sdq101 (djm3h, HackingPro1, etc)<br>
                    3. Click a "Execute" para juegos recomendados.
                    """,
         tags=["Recomendación"])
def recomendacion_juego_u(id_user: str):
    try:
        # Buscar las recomendaciones para el usuario
        recomendaciones = df_modelo_u[df_modelo_u['user_id'] == id_user]['recomendaciones'].iloc[0]

        # Verificar si la lista de recomendaciones no está vacía
        if len(recomendaciones) > 0:
            recomendaciones_dict = {i + 1: juego for i, juego in enumerate(recomendaciones)}
            return recomendaciones_dict
        else:
            return f"No hay recomendaciones disponibles para el usuario con ID {id_user}."

    except IndexError:
        # Manejar el caso en que el usuario no exista en el DataFrame
        return f"El usuario con ID {id_user} no existe en la base de datos."
 
