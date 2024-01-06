from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise        import cosine_similarity
from sklearn.metrics.pairwise        import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI(debug=True)

df = pd.read_csv('CSV/Unificado.csv')


# CONSULTAS


@app.get(path = '/',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Haga click en "Execute".<br>
                        3. Bajar hasta 'Responses'
                        """,
         tags=["Inicio"])
def Welcome():
    return {"PROYECTO INTEGRADOR 'MLOps' POR SANTIAGO RUEDA"}


@app.get(path = '/PlayTimeGenre',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género de videjuego.<br>
                        3. Haga click en "Execute".<br>
                        4. Bajar hasta 'Responses'
                        """,
         tags=["Consultas"])
def PlayTimeGenre(genre: str) -> dict:
    genre = genre.capitalize()
    df_genre = df[df[genre] == 1]
    df_year_play = df_genre.groupby('posted year')['playtime_forever'].sum().reset_index()
    max_play = df_year_play.loc[df_year_play['playtime_forever'].idxmax(), 'posted year']
    return {"Año de lanzamiento con más horas jugadas para Género '{}' ".format(genre): int(max_play)}



@app.get(path = '/UserForGenre',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género de videjuego.<br>
                        3. Haga click en "Execute".<br>
                        4. Bajar hasta 'Responses'
                        """,
         tags=["Consultas"])
def UserForGenre(genre: str) -> dict:
    genre = genre.capitalize()
    df_genre = df[df[genre] == 1]
    maxplay_user = df_genre.loc[df_genre['playtime_forever'].idxmax(), 'user_id']
    df_yearplay = df_genre.groupby('posted year')['playtime_forever'].sum().reset_index()
    list_play = df_yearplay .to_dict(orient='records')
    resultado = {
        "Usuario con más horas jugadas para Género " + genre: maxplay_user,
        "Horas jugadas": list_play}
    return resultado


@app.get(path = '/UsersRecommend',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el Año.<br>
                        3. Haga click en "Execute".<br>
                        4. Bajar hasta 'Responses'
                        """,
         tags=["Consultas"])
def UsersRecommend(year: int) -> dict:
    df_filtro = df[(df['posted year'] == year) & (df['recommend'] == True & (df['sentiment_analysis'] == 2))]
    if df_filtro.empty:
        return {"error": 'Valor no encontrado'}
    df_ordenado = df_filtro.sort_values(by='sentiment_analysis', ascending=False)
    top_reseñas = df_ordenado.head(3)
    resultado = {
        "TOP 1": top_reseñas.iloc[0]['title'],
        "TOP 2": top_reseñas.iloc[1]['title'],
        "TOP 3": top_reseñas.iloc[2]['title']
    }
    return resultado


@app.get(path = '/UsersWorstDeveloper',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el Año.<br>
                        3. Haga click en "Execute".<br>
                        4. Bajar hasta 'Responses'
                        """,
         tags=["Consultas"])
def UsersWorstDeveloper(year: int) -> dict:
    df_filtro = df[(df['posted year'] == year) & (df['recommend'] == False) & (df['sentiment_analysis'] <= 1)]
    if df_filtro.empty:
        return {"error": 'Valor no encontrado'}
    df_ordenado = df_filtro.sort_values(by='sentiment_analysis', ascending=False)
    top_3 = df_ordenado.head(3)
    resultado = {
        "TOP 1": top_3.iloc[0]['developer'],
        "TOP 2": top_3.iloc[1]['developer'],
        "TOP 3": top_3.iloc[2]['developer']
    }
    return resultado


@app.get(path = '/sentiment_analysis',
          description = """ <font color="green">
                        INDICACIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre de la desarrolladora.<br>
                        3. Haga click en "Execute".<br>
                        4. Bajar hasta 'Responses'
                        """,
         tags=["Consultas"])
def sentiment_analysis(developer: str) -> dict:
    df_filtro = df[df['developer'] == developer]
    conteo = df_filtro['sentiment_analysis'].value_counts()
    resultado = {
        "Positive": int(conteo.get(0, 0)),
        "Neutral": int(conteo.get(1, 0)),
        "Negative": int(conteo.get(2, 0))
    }
    return resultado



# RECOMENDACIONES



@app.get('/recomendacion_juego',
         description=""" <font color="green">
                    INDICACIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el id de producto.<br>
                    3. Haga click en "Execute".<br>
                    4. Bajar hasta 'Responses'
                    </font>
                    """,
         tags=["Recomendación"])

def recomendacion_juego(id_producto: int):

    # Creo una muestra a partir del df original para mejorar el desempeño del sistema de predicción ya que el original contiene muchos más datos
    muestra = df.head(6000)
    tfidf = TfidfVectorizer(stop_words='english')
    muestra = muestra.fillna("") 

    tdfid_matriz = tfidf.fit_transform(muestra['review'])
    cosine_similarity = linear_kernel( tdfid_matriz, tdfid_matriz)

    # Compruebo si el Id proporcionado existe en la muestra, si no, devuelvo un mensaje de error
    if id_producto not in muestra['id'].values:
        return {'Mensaje': 'No existe el id del juego.'}
    
    # Obtengo los géneros del juego de las columnas del df
    generos = muestra.columns[4:27]
    
    # Filtro para incluir juegos con géneros coincidentes pero con títulos diferentes
    filtered_df = muestra[(muestra[generos] == 1).any(axis=1) & (muestra['id'] != id_producto)]
    
    # Calculo similitud del coseno entre las reseñas de los juegos filtrados
    tdfid_matrix_filtered = tfidf.transform(filtered_df['review'])
    cosine_similarity_filtered = linear_kernel(tdfid_matrix_filtered, tdfid_matrix_filtered)
    
    # Genero una lista ordenando los valores de la lista de similitud del coseno de mayor a menor y seleccionando los 5 primeros juegos
    index = muestra[muestra['id'] == id_producto].index[0]
    sim_cosine = list(enumerate(cosine_similarity_filtered[index]))
    similar_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
    similar_ind = [i for i, _ in similar_scores[1:6]]
    similar_juegos = filtered_df['title'].iloc[similar_ind].values.tolist()
    
    return {'juegos recomendados': list(similar_juegos)}

