# <h1 align=center>**`Diccionario de datasets`**</h1>

 * **output_steam_games.json**  dataset que contiene datos relacionados con los juegos en general, como título,  desarrolladora, características técnicas, etiquetas, entre otros datos.

Las variables que contiene son:  
    * **publisher**: empresa publicadora del contenido.  
    * **genres**: género del item, es decir, del juego. Esta formado por una lista de uno o mas géneros por registro.  
    * **app_name**: nombre del item, es decir, del juego.  
    * **title**: título del item.  
    * **url**: url del juego.  
    * **release_date**: fecha de lanzamiento del item en formato 2018-01-04.  
    * **tags**: etiqueta del contenido. Esta formado por una lista de uno o mas etiquetas por registro.  
    * **reviews_url**: url donde se encuentra el review de ese juego.  
    * **specs**: especificaciones de cada item. Es una lista con uno o mas string con las especificaciones.  
    * **price**: precio del item.  
    * **early_access**: acceso temprano con un True/False.  
    * **id**: identificador único del juego.  
    * **developer**: desarrolladora del juego. 

* **australian_user_reviews.json**  dataset que contiene las reseñas de los usuarios realizados sobre los juegos que consumen, adicionalmente, como datos de si recomiendan o no ese juego. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comentó.

Las variables que contiene son:
    * **user_id**: identificador único para el usuario.  
    * **user_url**: url del perfil del usuario en streamcommunity.  
    * **reviews**: contiene una lista de diccionarios. Para cada usuario se tiene uno o más diccionarios con el review.  
    * **funny**: indica si alguien puso emoticón de 'funny' al review.  
    * **posted**: fecha de posteo del review en formato 'Posted April 21, 2011'.  
    * **last_edited**: fecha de la última edición.  
    * **item_id**: identificador único del item o juego.  
    * **helpful**: parámetro donde otros usuarios indican si fue útil la información.  
    * **recommend**: indica si el usuario recomienda o no el juego.  
    * **review**: sentencia string con los comentarios sobre el juego.  

* **australian_users_items.json**  dataset que contiene información sobre los juegos consumidos por todos los usuarios, así como el tiempo acumulado que cada usuario ha jugado en cada juego.

Las variables que contiene son:  
    * **user_id**: contiene un identificador único del usuario.  
    * **items_count**: número entero que indica la cantidad de juegos que ha consumido el usuario.  
    * **steam_id**: identificador único para la plataforma.  
    * **user_url**: url del perfil del usuario  
    * **items**: lista de uno o más diccionarios de los items que consume cada usuario.  
    * **item_id**: identificador del item o juego.  
    * **item_name**: nombre del juego.  
    * **playtime_forever**: tiempo acumulado que un usuario jugó a un juego.  
    * **playtime_2weeks**: tiempo acumulado que un usuario jugó en las últimas dos semanas.  
