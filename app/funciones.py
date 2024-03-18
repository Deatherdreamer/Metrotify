import os
import requests
import uuid
import json
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt



from .modelos import Usuario, Album, Cancion, Playlist


def generate_id():
    """
    Genera un UUID (Identificador Único Universal) versión 4.

    Devuelve:
        Un string que representa un UUID versión 4.
    """
    return str(uuid.uuid4())

def validate_if_username_exists(username):
    """
    Valida si un nombre de usuario ya existe en el archivo 'db/usuarios.json'.

    Parámetros:
        username (str): El nombre de usuario a validar.

    Devuelve:
        bool: True si el nombre de usuario ya existe, False si no.
    """
    with open("db/usuarios.json", "r") as file:
        users = json.load(file)

    for user in users:
        if user["username"] == username:
            return True

    return False

def validate_integer_input(prompt):
    """
    Solicita un valor entero al usuario y valida que sea un entero.

    Parámetros:
        prompt (str): El mensaje a mostrar al usuario.

    Devuelve:
        int: El valor entero ingresado por el usuario.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Por favor, ingrese un valor entero.")
            
def validate_integer_input_min_max(prompt, min_value, max_value):
    """
    Solicita un valor entero al usuario y valida que esté dentro de un rango.

    Parámetros:
        prompt (str): El mensaje a mostrar al usuario.
        min_value (int): El valor mínimo permitido.
        max_value (int): El valor máximo permitido.

    Devuelve:
        int: El valor entero ingresado por el usuario.
    """
    while True:
        value = validate_integer_input(prompt)
        if min_value <= value <= max_value:
            return value
        print(f"Por favor, ingrese un valor entre {min_value} y {max_value}.")
        
def validate_string_input(prompt):
    """
    Solicita un valor de texto al usuario y valida que no esté vacío.

    Parámetros:
        prompt (str): El mensaje a mostrar al usuario.

    Devuelve:
        str: El valor de texto ingresado por el usuario.
    """
    while True:
        value = input(prompt)
        if value:
            return value
        print("Por favor, ingrese un valor válido.")
    
def select_user_type():
    """
    Solicita al usuario seleccionar un tipo de usuario.

    El usuario puede seleccionar entre 'admin' y 'user'.

    Devuelve:
        str: El tipo de usuario seleccionado.
    """
    while True:
        print("Seleccione un tipo de usuario: ")
        print("1. Escucha")
        print("2. Músico")
        opc = validate_integer_input("Ingrese una opción: ")
        if opc == 1:
            return "listener"
        elif opc == 2:
            return "musician"
        else:
            print("Opción inválida.")


def restore_default_data():
    """
    Restaura los datos por defecto de la aplicación.

    La función carga los usuarios, álbumes y playlists desde una API y los guarda
    en los archivos 'db/usuarios.txt', 'db/albums.txt', 'db/canciones.txt' y 'db/playlists.txt'.

    Devuelve:
        Un diccionario con los códigos de estado de las respuestas HTTP de cada solicitud.
    """
    codes = {
        "users": load_users_from_api(),
        "albums": load_albums_from_api(),
        "playlists": load_playlists_from_api()
    }
    return codes
   

def load_users_from_api():
    """
    Carga los usuarios desde una API.

    La función realiza una solicitud GET a la API, parsea la respuesta a JSON,
    y luego escribe cada usuario en el archivo 'db/usuarios.json'. Cada usuario
    se escribe en una nueva línea en formato JSON.

    Al abrir el archivo 'db/usuarios.json' en modo escritura, se borra cualquier
    contenido existente en el archivo.

    Devuelve:
        El código de estado de la respuesta HTTP.
    """
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"
    response = requests.get(url)
    data = response.json()
    with open("db/usuarios.json", "w") as file:
        json_data = []
        for user in data:
            user = Usuario(user["id"], user["name"], user["email"], user["username"], user["type"])
            user_dict = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "type": user.type,
                "liked_albums": [],
                "songs_liked": [],
                "playlists": [],
                "artists_liked": []
            }
            json_data.append(user_dict)
        json.dump(json_data, file)
            
    return response.status_code

def load_albums_from_api():
    """
    Carga los álbumes desde una API y guarda la información en archivos JSON.

    Returns:
        int: El código de estado de la respuesta HTTP.
    """
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/albums.json"
    response = requests.get(url)
    data = response.json()

    all_tracks = []
    all_albums = []

    for album in data:
        album_dict = {
            "id": album["id"],
            "name": album["name"],
            "description": album["description"].replace('\n', ' '),
            "cover": album["cover"],
            "published": album["published"],
            "genre": album["genre"],
            "artist": album["artist"],
            "tracklist": [track["id"] for track in album["tracklist"]] 
        }
        all_albums.append(album_dict)

        for track in album["tracklist"]:
            track_dict = {
                "id": track["id"],
                "name": track["name"],
                "duration": track["duration"],
                "link": track["link"],
                "played": 0,
                "liked": 0
            }
            all_tracks.append(track_dict)                          
            

    with open("db/albums.json", "w") as file:
        json.dump(all_albums, file)

    with open("db/canciones.json", "w") as file:
        json.dump(all_tracks, file)

    return response.status_code

def load_playlists_from_api():
    """
    Carga las listas de reproducción desde una API y las guarda en un archivo JSON local.

    Returns:
        int: Código de estado de la respuesta HTTP.
    """
    url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/playlists.json"
    response = requests.get(url)
    data = response.json()

    with open("db/playlists.json", "w") as file:
        json_data = []
        for playlist in data:
            playlist_dict = {
                "id": playlist["id"],
                "name": playlist["name"],
                "description": playlist["description"].replace('\n', ' '),
                "creator": playlist["creator"],
                "tracks": playlist["tracks"]
            }
            json_data.append(playlist_dict)
        json.dump(json_data, file)

    return response.status_code

def load_all_data():
    """
    Carga todos los datos de la aplicación desde los archivos 'db/usuarios.json',
    'db/albums.json', 'db/canciones.json' y 'db/playlists.json'.

    Devuelve:
        Un diccionario con los datos cargados.
    """
    with open("db/usuarios.json") as file:
        users = json.load(file)
    with open("db/albums.json") as file:
        albums = json.load(file)
    with open("db/canciones.json") as file:
        songs = json.load(file)
    with open("db/playlists.json") as file:
        playlists = json.load(file)
        
    usuarios = [Usuario(**user) for user in users]
    
    albumes = [Album(**album) for album in albums]
    
    canciones = [Cancion(**song) for song in songs]
    
    playlists = [Playlist(**playlist) for playlist in playlists]
    
    return usuarios, albumes, canciones, playlists

def create_new_user():
    """
    Crea un nuevo usuario.

    La función solicita al usuario ingresar los datos del nuevo usuario, valida
    que el nombre de usuario no exista, y luego escribe el usuario en el archivo
    'db/usuarios.json'.

    Devuelve:
        Usuario: El objeto Usuario creado.
    """
    os.system('cls')
    print("Creación de nuevo usuario")
    id = generate_id()
    name = validate_string_input("Ingrese su nombre: ")
    email = validate_string_input("Ingrese su correo electrónico: ")
    username = validate_string_input("Ingrese un nombre de usuario: ")
    while validate_if_username_exists(username):
        print("El nombre de usuario ya existe. Por favor, ingrese otro.")
        username = validate_string_input("Ingrese un nombre de usuario: ")
    type = select_user_type()
    user = Usuario(id, name, email, username, type)

    with open("db/usuarios.json", "r") as file:
        users = json.load(file)

    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "type": user.type,
        "liked_albums": [],
        "songs_liked": [],
        "playlists": [],
        "artists_liked": []
    }

    users.append(user_dict)

    with open("db/usuarios.json", "w") as file:
        json.dump(users, file)

    return user

def login_user():
    """
    Inicia sesión de un usuario.

    La función solicita al usuario ingresar su nombre de usuario y luego
    busca el usuario en el archivo 'db/usuarios.json'.

    Devuelve:
        Usuario: El objeto Usuario que inició sesión.
    """
    username = validate_string_input("Ingrese su nombre de usuario: ")
    with open("db/usuarios.json", "r") as file:
        users = json.load(file)

    for user in users:
        if user["username"] == username:
            user = Usuario(**user)
            print(f"Bienvenido, {user.name}!")
            user_menu(user)

    print("Usuario no encontrado.")
    return None

def user_menu(user):
    """
    Muestra el menú de opciones para un usuario.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    while True:
        os.system('cls')
        print("Menú de usuario")
        print(f"Bienvenido, {user.name}!")
        if user.type == "listener":
            print("1. Buscar Perfil")
            print("2. Buscar Canciones por Nombre, Album, Artista o Playlist")
            print("3. Crear playlist")
            print("4. Editar Usuario")
            print("5. Eliminar Cuenta")
            print("6. Salir")
            opc = validate_integer_input("Ingrese una opción: ")
            if opc == 1:
                search_user_profile(user)
            elif opc == 2:
                search_songs_menu(user)
            elif opc == 3:
                create_playlist(user)
            elif opc == 4:
                edit_user(user)
            elif opc == 5:
                delete_account(user)
                break
            elif opc == 6:
                print("Saliendo del menú de usuario...")
                break
            else:
                print("Opción inválida.")
        else:
            print("1. Buscar Perfil")
            print("2. Buscar Canciones por Nombre, Album, Artista o Playlist")
            print("3. Crear nuevo album")
            print("4. Editar Usuario")
            print("5. Eliminar Cuenta")
            print("6. Salir")
            opc = validate_integer_input("Ingrese una opción: ")
            if opc == 1:
                search_user_profile(user)
            elif opc == 2:
                search_songs_menu(user)
            elif opc == 3:
                create_album(user)
            elif opc == 4:
                edit_user(user)
            elif opc == 5:
                delete_account(user)
                break
            elif opc == 6:
                print("Saliendo del menú de usuario...")
                break
            else:
                print("Opción inválida.")

def create_album(user):
    """
    Crea un álbum.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    name = validate_string_input("Ingrese el nombre del álbum: ")
    description = validate_string_input("Ingrese la descripción del álbum: ")
    cover = validate_string_input("Ingrese la URL de la portada del álbum: ")
    published = validate_string_input("Ingrese la fecha de publicación del álbum: ")
    genre = validate_string_input("Ingrese el género del álbum: ")
    tracklist = []
    while True:
        print("Menú de creación de álbum")
        print("1. Agregar canción")
        print("2. Terminar")
        opc = validate_integer_input("Ingrese una opción: ")
        if opc == 1:
            track = create_track()
            tracklist.append(track.id)
        elif opc == 2:
            break
        else:
            print("Opción inválida.")
            
    with open("db/albums.json", "r") as file:
        albums = json.load(file)
        
    new_album = {
        "id": len(albums) + 1,
        "name": name,
        "description": description,
        "cover": cover,
        "published": published,
        "genre": genre,
        "artist": user.id,
        "tracklist": tracklist
    }
    
    albums.append(new_album)
    
    with open("db/albums.json", "w") as file:
        json.dump(albums, file, indent=4)
        
    print(f"Álbum {name} creado exitosamente.")
    
def create_track():
    """
    Crea una canción.

    Devuelve:
        Cancion: El objeto Cancion creado.
    """
    name = validate_string_input("Ingrese el nombre de la canción: ")
    duration = validate_string_input("Ingrese la duración de la canción: ")
    link = validate_string_input("Ingrese el enlace de la canción: ")

    with open("db/canciones.json", "r") as file:
        songs = json.load(file)
        
    new_song = {
        "id": len(songs) + 1,
        "name": name,
        "duration": duration,
        "link": link,
        "played": 0,
        "liked": 0
    }
    
    songs.append(new_song)
    
    with open("db/canciones.json", "w") as file:        
        json.dump(songs, file, indent=4)        
    print(f"Canción {name} creada exitosamente.")
    return Cancion(**new_song)


        


                
            
def create_playlist(user):
    """
    Crea una playlist.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    name = validate_string_input("Ingrese el nombre de la playlist: ")
    description = validate_string_input("Ingrese la descripción de la playlist: ")

    with open("db/canciones.json", "r") as file:
        all_songs = json.load(file)
        
    all_songs = [Cancion(**song) for song in all_songs]

    tracks = []
    while True:
        song_name = input("Ingrese el nombre de una canción para agregar a la playlist, o 'q' para terminar: ")
        if song_name.lower() == 'q':
            break
        matching_songs = [song for song in all_songs if song_name in song.name]
        if matching_songs:
            for i, song in enumerate(matching_songs, start=1):
                print(f"{i}. {song}")
            song_number = int(input("Seleccione una canción para agregar a la playlist: "))
            tracks.append(matching_songs[song_number - 1].id)
        else:
            print("No se encontraron canciones que coincidan.")

    with open("db/playlists.json", "r") as file:
        playlists = json.load(file)

    new_playlist = {
        "id": len(playlists) + 1,
        "name": name,
        "description": description,
        "creator": user.id,
        "tracks": tracks
    }

    playlists.append(new_playlist)

    with open("db/playlists.json", "w") as file:
        json.dump(playlists, file, indent=4)
        
    print(f"Playlist {name} creada exitosamente.")
    
def edit_user(user):
    """
    Edita un usuario.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    print("Menú de edición de usuario")
    print("1. Editar nombre")
    print("2. Editar correo electrónico")
    print("3. Editar nombre de usuario")
    print("4. Salir")
    opc = validate_integer_input("Ingrese una opción: ")
    if opc == 1:
        new_name = validate_string_input("Ingrese el nuevo nombre: ")
        user.edit_name(new_name)
        print("Nombre editado exitosamente.")
    elif opc == 2:
        new_email = validate_string_input("Ingrese el nuevo correo electrónico: ")
        user.edit_email(new_email)
        print("Correo electrónico editado exitosamente.")
    elif opc == 3:
        new_username = validate_string_input("Ingrese el nuevo nombre de usuario: ")
        while validate_if_username_exists(new_username):
            print("El nombre de usuario ya existe. Por favor, ingrese otro.")
            new_username = validate_string_input("Ingrese un nombre de usuario: ")
        user.edit_username(new_username)
        print("Nombre de usuario editado exitosamente.")
    elif opc == 4:
        print("Saliendo del menú de edición de usuario...")
    else:
        print("Opción inválida.")
        
def delete_account(user):
    """
    Elimina un usuario.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    confirm = input("Está a punto de eliminar su cuenta. ¿Está seguro? (s/n): ")
    if confirm.lower() == 's':
        with open("db/usuarios.json", "r") as file:
            users = json.load(file)

        users = [u for u in users if u["id"] != user.id]

        with open("db/usuarios.json", "w") as file:
            json.dump(users, file, indent=4)

        print("Cuenta eliminada exitosamente.")
        exit()
    else:
        print("Operación cancelada.")
        
            
            
def search_user_profile(user):
    """
    Busca un perfil de usuario por nombre.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    name = validate_string_input("Ingrese el nombre a buscar: ")
    with open("db/usuarios.json", "r") as file:
        users = json.load(file)

    matching_profiles = [user_profile for user_profile in users if name.lower() in user_profile["name"].lower() and user_profile["username"] != user.username]

    if matching_profiles:
        print("Perfiles encontrados:")
        for i, user_profile in enumerate(matching_profiles, start=1):
            print(f"{i:2d}. {user_profile['name']} ({user_profile['type']})")

        selection = validate_integer_input_min_max("Seleccione el perfil que desea ver: ", 1, len(matching_profiles))
        selected_profile = Usuario(**matching_profiles[selection - 1])
        show_user_profile(selected_profile)
    else:
        print("Perfil no encontrado.")
        input("Presione Enter para continuar...")
        
        
        
def show_user_profile(user):
    """
    Muestra el perfil de un usuario.

    Parámetros:
        user (Usuario): El objeto Usuario a mostrar.
    """
    os.system('cls')
    print("***Perfil de usuario***")
    print(f"Nombre: {user.name}")
    if user.type == "listener":
        print("Tipo: Escucha")
        print("Artistas que le gustan:")
        for artist in user.get_liked_artists():
            print(f"- {artist.name}")
        print("Álbumes que le gustan:")
        for album in user.get_liked_albums():
            print(f"- {album.name} de {album.get_artist()}")
        print("Canciones que le gustan:")
        for song in user.get_liked_songs():
            print(f"- {song.name} del álbum {song.get_album()} de {song.get_artist()}")
    else:
        user.show_albums()
        print("Canciones mas escuchadas:")
        for song in user.get_top_songs():
            print(f"- {song.name} Reproducciones: {song.played} Likes: {song.liked}")
        print("Cantidad de reproducciones Totales: ", user.get_total_played())
    
    input("Presione Enter para continuar...")
    
        
def search_songs_menu(user):
    """
    Muestra el menú de búsqueda de canciones.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    while True:
        os.system('cls')
        print("Menú de búsqueda de canciones")
        print("1. Buscar por Nombre")
        print("2. Buscar por Album")
        print("3. Buscar por Artista")
        print("4. Buscar por Playlist")
        print("5. Salir")
        opc = validate_integer_input("Ingrese una opción: ")
        if opc == 1:
            search_songs_by_name(user)
        elif opc == 2:
            search_songs_by_album(user)
        elif opc == 3:
            search_songs_by_artist(user)
        elif opc == 4:
            search_songs_by_playlist(user)
        elif opc == 5:
            print("Saliendo del menú de búsqueda de canciones...")
            break
        else:
            print("Opción inválida.")
            
            
def search_songs_by_name(user):
    """
    Busca canciones por nombre.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    name = validate_string_input("Ingrese el nombre de la canción a buscar: ")
    with open("db/canciones.json", "r") as file:
        songs = json.load(file)

    matching_songs = [Cancion(**song) for song in songs if name.lower() in song["name"].lower()]

    if matching_songs:
        print("Canciones encontradas:")
        for i, song in enumerate(matching_songs, start=1):
            print(f"{i:2d}. {song}")
        selection = validate_integer_input_min_max("Seleccione la canción que desea ver: ", 1, len(matching_songs))
        selected_song = matching_songs[selection - 1]
        show_song(selected_song, user)
    else:
        print("Canción no encontrada.")
        
def search_songs_by_album(user):
    """
    Busca canciones por álbum.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    album_name = validate_string_input("Ingrese el nombre del álbum a buscar: ")
    with open("db/albums.json", "r") as file:
        albums = json.load(file)

    matching_albums = [Album(**album) for album in albums if album_name.lower() in album["name"].lower()]

    if matching_albums:
        print("Álbumes encontrados:")
        for i, album in enumerate(matching_albums, start=1):
            print(f"{i:2d}. {album.name} - {album.published}")
        selection = validate_integer_input_min_max("Seleccione el álbum que desea ver: ", 1, len(matching_albums))
        selected_album = matching_albums[selection - 1]
        show_album(selected_album, user)
    else:
        print("Álbum no encontrado.")

def search_songs_by_artist(user):
    """
    Busca canciones por artista.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    artist_name = validate_string_input("Ingrese el nombre del artista a buscar: ")
    with open("db/usuarios.json", "r") as file:
        users = json.load(file)

    matching_artists = [Usuario(**user) for user in users if artist_name.lower() in user["name"].lower() and user["type"] == "musician"]

    if matching_artists:
        print("Artistas encontrados:")
        for i, artist in enumerate(matching_artists, start=1):
            print(f"{i:2d}. {artist.name}")
        selection = validate_integer_input_min_max("Seleccione el artista que desea ver: ", 1, len(matching_artists))
        selected_artist = matching_artists[selection - 1]
        show_artist(selected_artist, user)
    else:
        print("Artista no encontrado.")

def search_songs_by_playlist(user):
    """
    Busca canciones por playlist.

    Parámetros:
        user (Usuario): El objeto Usuario que inició sesión.
    """
    playlist_name = validate_string_input("Ingrese el nombre de la playlist a buscar: ")
    with open("db/playlists.json", "r") as file:
        playlists = json.load(file)

    matching_playlists = [Playlist(**playlist) for playlist in playlists if playlist_name.lower() in playlist["name"].lower()]

    if matching_playlists:
        print("Playlists encontradas:")
        for i, playlist in enumerate(matching_playlists, start=1):
            print(f"{i:2d}. {playlist.name}")
        selection = validate_integer_input_min_max("Seleccione la playlist que desea ver: ", 1, len(matching_playlists))
        selected_playlist = matching_playlists[selection - 1]
        show_playlist(selected_playlist, user)
    else:
        print("Playlist no encontrada.")
        
def show_album(album, user):
    """
    Muestra un álbum.

    Parámetros:
        album (Album): El objeto Album a mostrar.
    """
    os.system('cls')
    print(f"Álbum: {album.name}")
    print(f"Artista: {album.artist}")
    print(f"Descripción: {album.description}")
    print(f"Género: {album.genre}")
    print(f"Fecha de publicación: {album.published}")

    while True:
        print("1. Ver canciones")
        if album.verify_if_liked(user):
            print("2. Ya no me gusta este álbum")
        else:
            print("2. Me gusta este álbum")            
        print("3. Retroceder")
        option = input("Escoge una Opcion: ")

        if option == "1":
            show_album_songs(album, user)
        elif option == "2":
            if album.verify_if_liked(user):
                print(f"Ya no te gusta {album.name}")
                user.dislike_album(album)
            else:
                print(f"Te gusta {album.name}")
                user.like_album(album)
            
        elif option == "3":
            break
        else:
            print("Opcion invalida. Intente nuevamente.")
            

def show_album_songs(album, user):
    """
    Muestra las canciones de un álbum y permite al usuario seleccionar una para mostrar.

    Parámetros:
        album (Album): El objeto Album del cual mostrar las canciones.
    """
    print("     ***Canciones del Álbum:***")
    songs = album.get_songs()
    for count, song in enumerate(songs, start=1):
        print(f"{count}. {song.name}")

    song_number = int(input("Seleccione una canción para mostrar: "))
    selected_song = songs[song_number - 1]
    show_song(selected_song, user)
    
def show_artist(artist, user):
    """
    Muestra un artista.

    Parámetros:
        artist (Usuario): El objeto Usuario que representa al artista.
    """
    os.system('cls')
    print(f"Artista: {artist.name}")
    while True:
        print("1. Ver álbumes")
        if artist.verify_if_liked(user):
            print("2. Ya no me gusta este artista")
        else:
            print("2. Me gusta este artista")
        
        print("3. Retroceder")
        option = input("Escoge una Opcion: ")

        if option == "1":
            show_artist_albums(artist, user)
        elif option == "2":
            if artist.verify_if_liked(user):
                print(f"Ya no te gusta {artist.name}")
                user.dislike_artist(artist)
            else:
                print(f"Te gusta {artist.name}")
                user.like_artist(artist)
            
        elif option == "3":
            break
        else:
            print("Opcion invalida. Intente nuevamente.")
    
    
def show_artist_albums(artist, user):
    """
    Muestra los álbumes de un artista y permite al usuario seleccionar uno para mostrar.

    Parámetros:
        artist (Usuario): El objeto Usuario que representa al artista.
    """
    print("     ***Álbumes del Artista:***")
    albums = artist.get_albums()
    for count, album in enumerate(albums, start=1):
        print(f"{count}. {album.name}")

    album_number = int(input("Seleccione un álbum para mostrar: "))
    selected_album = albums[album_number - 1]
    show_album(selected_album, user)
    
def show_playlist(playlist, user):
    """
    Muestra una playlist.

    Parámetros:
        playlist (Playlist): El objeto Playlist a mostrar.
    """
    os.system('cls')
    print(f"Playlist: {playlist.name}")
    print(f"Creada por: {playlist.creator}")
    print(f"Descripción: {playlist.description}")
    print("Canciones:")
    for count, track in enumerate(playlist.get_tracks(), start=1):
        print(f"{count}. {track}")
        
    while True:
        print("1 Seleccionar una canción para reproducir")
        print("2. Retroceder")
        option = validate_integer_input("Ingrese una opción: ")
        if option == 1:
            song_number = validate_integer_input_min_max("Seleccione una canción para reproducir: ", 1, len(playlist.tracks))
            selected_song = playlist.get_tracks()[song_number - 1]
            show_song(selected_song, user)
        elif option == 2:
            break
        else:
            print("Opción inválida.")
         
            
            

def show_song(song, user):
    """
    Muestra una canción.

    Parámetros:
        song (Cancion): El objeto Cancion a mostrar.
    """
    os.system('cls')
    print(f"Canción: {song.name}")
    while True:
        if song.verify_if_liked(user):
            print("1. Quitar me gusta.")
            
        else:
            print("1. Me gusta esta canción.")
            
            
        print("2. Play this song")
        print("3. Retroceder")
        option = input("Escoge una Opcion: ")

        if option == "1":
            if song.verify_if_liked(user):
                print(f"Ya no te gusta {song.name}")
                user.dislike_song(song)
            else:
                print(f"Te gusta {song.name}")
                user.like_song(song)
        elif option == "2":
            webbrowser.open(song.link)
            song.play()
        elif option == "3":
            break
        else:
            print("Opcion invalida. Intente nuevamente.")
    
def show_statistics():

    usuarios, albumes, canciones, playlists = load_all_data()
    
    musicians = pd.DataFrame([{'name': user.name, 'streams': user.get_total_played()} for user in usuarios if user.type == "musician"])
    albums = pd.DataFrame([{'name': album.name, 'streams': album.get_total_streams()} for album in albumes])
    songs = pd.DataFrame([{'name': song.name, 'streams': song.played} for song in canciones])

    top_musicians = musicians.nlargest(5, 'streams')
    print(top_musicians)

    top_albums = albums.nlargest(5, 'streams')
    print(top_albums)

    top_songs = songs.nlargest(5, 'streams')
    print(top_songs)


    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    axs[0].bar(top_musicians['name'], top_musicians['streams'])
    axs[0].set_title('Top 5 Musicos con mas reproducciones')

    axs[1].bar(top_albums['name'], top_albums['streams'])
    axs[1].set_title('Top 5 Albums con mas reproducciones')

    axs[2].bar(top_songs['name'], top_songs['streams'])
    axs[2].set_title('Top 5 Songs mas escuchadas')


    plt.tight_layout()
    plt.show()