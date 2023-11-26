
import pandas as pd
#from textblob import TextBlob
import re

#----------------------verificar_tipo_datos-------------------------------------#
def verificar_tipo_datos(df):
    diccionario = {"Columna": [], "Tipo": [], "NO_nulos_%": [], "Nulos_%": [], "Nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        diccionario["Columna"].append(columna)
        diccionario["Tipo"].append(df[columna].apply(type).unique())
        diccionario["NO_nulos_%"].append(round(porcentaje_no_nulos, 2))
        diccionario["Nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        diccionario["Nulos"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(diccionario)
        
    return df_info

#-----------------------mostrar_filas_duplicadas-------------------------------#
def  mostrar_filas_duplicadas(df, columna):
    # Se filtran las filas duplicadas
    duplicated_filas = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_filas.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_filas_sorted = duplicated_filas.sort_values(by=columna)
    return duplicated_filas_sorted

#------------------------obtener_release_year-----------------------------------#
def obtener_release_year(fecha):
    # Verifica si la fecha no es un valor nulo
    if pd.notna(fecha):
        # Verifica si la fecha sigue el formato 'YYYY-MM-DD' utilizando una expresión regular
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            # Si la fecha cumple con el formato, extrae el año utilizando split
            return fecha.split('-')[0]
    
    # Si la fecha es nula o no sigue el formato esperado, devuelve 'Dato no disponible'
    return 'Dato no disponible'


#-------------------------get_sentimiento---------------------------------------#
def get_sentimiento(texto):
    if texto is None:
        return 1
    analysis = TextBlob(texto)
    polarity = analysis.sentiment.polarity
    if polarity < -0.5:
        return 0  
    elif polarity > 0.5: 
        return 2 
    else:
        return 1 

#--------------------------valor_en_porcentaje----------------------------------#
def valor_en_porcentaje(df, columna):
    cantidad = df[columna].value_counts()
    porcentaje = round(100 * cantidad / len(df),2)
    df_total = pd.DataFrame({
        "Cantidad": cantidad,
        "Porcentaje": porcentaje.map("{:.2f}%".format)
    })
    return df_total

#----------------------------valores_atipicos-----------------------------------#
def valores_atipicos(columna):
    # Cuartiles
    q1 = columna.describe()[4]
    q3 = columna.describe()[6]

    # Valor del vigote
    bigote_max = round(q3 + 1.5*(q3 - q1), 2)
    
    # Cantidad de atípicos
    print(f'Hay {(columna > bigote_max).sum()} valores atípicos')

    #-------------------------columna_rating------------------------------------#
def columna_rating(fila):
    ''' 
    - 1: si sa=0 y r=False
    - 2: si sa=1 y r=True
    - 2: si sa=2 y r=True
    '''
    if fila["sentiment_analysis"] == 0 and not fila["recommend"]:
        return 1
    elif fila["sentiment_analysis"] == 1 and fila["recommend"]:
        return 2
    elif fila["sentiment_analysis"] == 2 and fila["recommend"]:
        return 2
    else:
        return None
    
    #-------------------------------------------------------------------#

    
