<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h1 align=center> -DATA FT17-G06- </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

<hr>

# INTRODUCCION

<p style="text-align: justify;">Este proyecto se enfoca en la simulación del papel dual de un Data Science y Data Engineer para la renombrada plataforma internacional de juegos, Steam. Durante mi participación en este proyecto, asumí roles clave que abarcaron desde la ingeniería de datos hasta el despliegue de modelos de Machine Learning. La tarea principal consistió en trabajar con conjuntos de datos proporcionados para desarrollar un Producto Mínimo Viable (PMV).</p>

<p style="text-align: justify;">El PMV final incluye la implementación de una API alojada en un servicio en la nube, con la capacidad de realizar dos funciones esenciales de Machine Learning. En primer lugar, se abordó un análisis de sentimientos sobre los comentarios de los usuarios de los juegos, brindando insights valiosos sobre la recepción y la experiencia del usuario. En segundo lugar, se desarrolló un sistema de recomendación de juegos que opera tanto a partir del nombre de un juego como de las preferencias específicas de un usuario.</p>

<hr>

#  DESARROLLO

- ## Datos con los que se contaba
Se proporcionaron 3 archivos JSON:
<p style="text-align: justify;">
1) <b><u>output_steam_games.json</b></u>: dataset juegos. Contiene título, desarrollador, precios, etc.</br>
2) <b><u> australian_users_items.json</b></u>: dataset con información sobre los juegos que juegan los usuarios, tiempo acumulado por juego.</br>
3) <b><u>australian_user_reviews.json</b></u>: dataset con comentarios de los usuarios sobre los juegos que consumen,y datos adicionales como si recomiendan o no, la url del usuario y el id del juego que comenta.
4) <b><u>Diccionario</b></u>: variables de los dataset con información detallada de las mismas </p>


- ## Tareas que se realizaron

### 1 Transformaciones:
 <p style="text-align: justify;"> 
 ETL - Extracción, Transformación y Carga -: de los tres conjuntos de datos entregados. Inicialmente, me enfrenté al desafío de manejar archivos JSON y buscar alternativas efectivas para su lectura. Al analizar los conjuntos de datos, identifiqué la presencia de columnas anidadas, lo que requirió una estrategia específica para desanidarlas y convertirlas en columnas independientes.
 <p style="text-align: justify;"> 
Durante el proceso de transformación, me encontré con la necesidad de lidiar con filas completas de valores nulos, por lo que implementé acciones para eliminar estas instancias y garantizar la integridad de los datos restantes. Además, abordé la tarea de rellenar campos vacíos, asegurando que las variables esenciales para el proyecto estuvieran completas y listas para su utilización.
 <p style="text-align: justify;"> 
Con el objetivo de optimizar el rendimiento de la API y considerando las limitaciones de almacenamiento en el despliegue, adopté la estrategia de eliminar columnas insignificantes o aquellas con una cantidad significativa de valores nulos. Este enfoque se basó en una evaluación cuidadosa de la contribución de cada columna al desarrollo del proyecto.

<hr>

### 2 Feature Engineering:

 <p style="text-align: justify;"> 
Para el conjunto de datos user_reviews, se creó una nueva columna denominada 'sentiment_analysis', con el propósito de cuantificar el sentimiento asociado a las reseñas de juegos realizadas por diversos usuarios. Para lograr esto, se empleó la biblioteca de procesamiento de lenguaje natural (NLP) llamada TextBlob.
 <p style="text-align: justify;">
TextBlob permite calcular la polaridad de sentimiento de un texto y, en este contexto, se utilizó para asignar valores numéricos a las reseñas en función de su tono emocional. Específicamente, se estableció una escala de tres categorías: '0' para reseñas con sentimiento negativo, '1' para reseñas neutrales, y '2' para reseñas con sentimiento positivo.
 <p style="text-align: justify;">
Para determinar estas categorías, se establecieron umbrales de polaridad en -0.5 y 0.5. Las reseñas con polaridad por debajo de -0.5 fueron clasificadas como negativas, aquellas con polaridad por encima de 0.5 como positivas, y las reseñas con polaridad entre estos valores fueron consideradas neutrales.

<hr>

### 3 Analisis:
 <p style="text-align: justify;"> 
EDA - Análisis Exploratorio de Datos- el enfoque se centró en la identificación de variables clave para la creación del modelo de recomendación.
 <p style="text-align: justify;"> 
Se llevó a cabo un minucioso examen de las variables consideradas cruciales y apropiadas para el desarrollo de mi modelo de recomendaciones. Se prestó especial atención a factores que se percibieron como esenciales para entender los patrones de comportamiento y las preferencias de los usuarios. 
 <p style="text-align: justify;"> 
Adicionalmente, se exploraron otras variables con el objetivo de analizar su comportamiento y evaluar su posible impacto en el modelo de recomendación. Este enfoque amplio permitió obtener una comprensión integral de los datos, identificando no solo las variables críticas para el modelo, sino también aquellas que podrían proporcionar información valiosa sobre diversos aspectos del conjunto de datos.
<hr>

### 4 Modelo ML:
 <p style="text-align: justify;"> 
se optó por aplicar la medida de similitud del coseno, una técnica que evalúa la similitud entre elementos al calcular el coseno del ángulo entre sus vectores representativos. En este contexto, se abordaron dos enfoques distintos: ítem-ítem y user_item.
 <p style="text-align: justify;"> 
En el primer caso, el modelo se fundamenta en una relación <b>ítem-ítem</b>, donde se selecciona un juego como referencia y se evalúa su similitud con el resto de los juegos en función de las variables género y título. La recomendación se realiza sobre la base de qué tan cercanos son estos juegos en términos de características específicas.
 <p style="text-align: justify;"> 
En el segundo caso, el modelo adopta un enfoque de filtro <b>user-item</b>, identificando usuarios similares a un usuario de referencia y recomendando juegos que hayan sido apreciados por esos usuarios similares. Aquí, la similitud del coseno se emplea para medir la proximidad entre perfiles de usuarios, facilitando la generación de recomendaciones personalizadas.

<hr>

### 5 Desarrollo API

 <p style="text-align: justify;"> 
Se requirió del desarrollo de las siguientes funciones:

1. PlayTimeGenre(genero: str)
 <p style="text-align: justify;"> 
Esta función devuelve el año con más horas jugadas para un género específico. La información se presenta en un diccionario con el formato: {"Año de lanzamiento con más horas jugadas para Género X": 2013}. 

2. UserForGenre(genero: str)
 <p style="text-align: justify;"> 
Esta función retorna el usuario que acumula más horas jugadas para el género proporcionado, junto con una lista que muestra la acumulación de horas jugadas por año. El resultado se presenta en un diccionario de la forma: {"Usuario con más horas jugadas para Género X": us213ndjss09sdf, "Horas jugadas": [{"Año": 2013, "Horas": 203}, {"Año": 2012, "Horas": 100}, {"Año": 2011, "Horas": 23}]}.

3. UsersRecommend(año: int)
 <p style="text-align: justify;"> 
Esta función devuelve el top 3 de juegos más recomendados por usuarios para el año especificado. Se consideran solo aquellos juegos con revisiones marcadas como recomendadas y comentarios positivos o neutrales. El resultado se presenta en una lista de diccionarios, donde cada diccionario tiene el formato: {"Puesto 1": X}, {"Puesto 2": Y}, {"Puesto 3": Z}.

4. UsersWorstDeveloper(año: int)
 <p style="text-align: justify;"> 
La función proporciona el top 3 de desarrolladoras con juegos menos recomendados por usuarios para el año dado. Se consideran solo aquellos juegos con revisiones marcadas como no recomendadas y comentarios negativos. La salida se presenta en una lista de diccionarios similar.

5. sentiment_analysis(empresa_desarrolladora: str)
 <p style="text-align: justify;"> 
La función realiza un análisis de sentimiento según la empresa desarrolladora, devolviendo un diccionario con el nombre de la desarrolladora como clave y una lista que muestra la cantidad total de registros de reseñas de usuarios categorizados con un análisis de sentimiento como valor. El formato del resultado es: {'Valve': [Negative = 182, Neutral = 120, Positive = 278]}. 

6. recomendacion_juego(id_producto: str)
 <p style="text-align: justify;"> 
La función está diseñada para un sistema de recomendación item-item. A partir del id_producto se devuelve una lista con 5 juegos recomendados que son similares al producto ingresado. El resultado se presenta como [Juego Recomendado 1, Juego Recomendado 2, Juego Recomendado 3, Juego Recomendado 4, Juego Recomendado 5]. 

7. recomendacion_usuario(id_usuario: str)
 <p style="text-align: justify;"> 
Esta última función está destinada a un sistema de recomendación user-item. A partir del ID de un usuario, la se genera una lista con 5 juegos recomendados específicamente para ese usuario. El resultado: [Juego Recomendado 1, Juego Recomendado 2, Juego Recomendado 3, Juego Recomendado 4, Juego Recomendado 5].
 <p style="text-align: justify;"> 
Es importante destacar que todas estas funciones fueron implementadas en un entorno virtual de FastAPI y se desplegaron en la plataforma Render utilizando la versión gratuita. Para optimizar el rendimiento en este entorno, se generaron dataframes más pequeños que aún así ofrecían información valiosa y podían ser consumidos eficientemente.
<hr>

#  INFORMACION ADICIONAL

En los archivos proporcionados del desarrollo de este trabajo se encuentran en:

- API: 
  - Funciones:[Enlace](https://github.com/magamahae/TRABAJO_I_I/blob/main/SCR/API_tablas_funciones.ipynb)
  - Deploy: [enlace](https://trabajo-deploy.onrender.com/)
- MODELO:
  - Jupyter Notebook:
- ETL/EDA:
  - Jupyter Nootebok:
- VIDEO:
  - Link:

<hr>

# TECNOLOGIAS

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)
<hr>

# CONCLUSION
 <p style="text-align: justify;"> 
En el transcurso de este proyecto, el objetivo primordial fue la creación y presentación de un Producto Mínimo Viable (PMV) para la plataforma de juegos Steam. Se llevaron a cabo análisis fundamentales con la intención de establecer las bases para desarrollos más amplios en futuras etapas.
 <p style="text-align: justify;"> 
Se identificó la necesidad de mejorar ciertos aspectos del proyecto en próximas fases. Uno de los puntos clave a considerar es la posibilidad de investigar y completar datos faltantes, así como mejorar la calidad general de los datos. Este paso resulta esencial para garantizar la robustez y confiabilidad de cualquier modelo o análisis subsiguiente.
 <p style="text-align: justify;"> 
Además, se observó que la información temporal en el conjunto de datos podría beneficiarse de una actualización. Dada la evolución constante de la industria de los videojuegos, las fechas de lanzamiento y otros datos temporales quedaron relativamente desactualizados. Por lo tanto, la incorporación de datos más recientes podría proporcionar una representación más precisa de la realidad del mercado.
 <p style="text-align: justify;"> 
En resumen, este proyecto marcó un primer paso significativo hacia la comprensión y aplicación de técnicas de Data Science en el contexto de la plataforma Steam. Si bien se logró un PMV funcional, queda claro que hay oportunidades para la expansión y mejora continua en futuras iteraciones. El enfoque en la completitud y calidad de los datos, así como la actualización temporal, representa áreas clave para explorar y perfeccionar en el desarrollo futuro de este proyecto.
<hr>
Gracias por vuestra atención...</br>
 
Saluda atte,
 <p style="text-align: center;"> 
                                     Ma. Gabriela
