import json

class Usuario():
    """
    Una clase para representar un usuario.

    ...

    Atributos
    ----------
    id : str
        un identificador único para el usuario
    name : str
        el nombre del usuario
    email : str
        el correo electrónico del usuario
    username : str
        el nombre de usuario del usuario
    type : str
        el tipo de usuario
    liked_albums : list
        una lista de identificadores de álbumes que le gustan al usuario
    songs_liked : list
        una lista de identificadores de canciones que le gustan al usuario
    playlists : list
        una lista de identificadores de listas de reproducción creadas por el usuario
    artists_liked : list
        una lista de identificadores de artistas que le gustan al usuario

    Métodos
    -------
    to_dict():
        Devuelve una representación de diccionario del usuario.
    like_album(album_id):
        Agrega el identificador del álbum a los álbumes que le gustan al usuario.
    like_song(song):
        Agrega el identificador de la canción a las canciones que le gustan al usuario.
    like_artist(artist_id):
        Agrega el identificador del artista a los artistas que le gustan al usuario.
    dislike_album(album_id):
        Elimina el identificador del álbum de los álbumes que le gustan al usuario.
    dislike_song(song):
        Elimina el identificador de la canción de las canciones que le gustan al usuario.
    dislike_artist(artist_id):
        Elimina el identificador del artista de los artistas que le gustan al usuario.
    show_albums():
        Imprime los álbumes del artista.
    show_songs():
        Imprime las canciones del artista.
    get_albums():
        Devuelve una lista de álbumes del artista.
    get_songs():
        Devuelve una lista de canciones del artista.
    edit_name(new_name):
        Cambia el nombre del usuario.
    edit_email(new_email):
        Cambia el correo electrónico del usuario.
    edit_username(new_username):
        Cambia el nombre de usuario del usuario.
    get_liked_albums():
        Devuelve una lista de álbumes que le gustan al usuario.
    get_liked_songs():
        Devuelve una lista de canciones que le gustan al usuario.
    get_liked_artists():
        Devuelve una lista de artistas que le gustan al usuario.
    get_playlists():
        Devuelve una lista de listas de reproducción creadas por el usuario.
    get_amount_likes():
        Devuelve el número total de "me gusta" recibidos por el artista.
    verify_if_liked(user_id):
        Verifica si el usuario ha dado "me gusta" al artista.
    get_top_songs():
        Devuelve las 10 canciones más reproducidas del artista.
    get_total_played():
        Devuelve el número total de veces que se han reproducido las canciones del artista.
    """
    def __init__(self, id, name, email, username, type, liked_albums = [], songs_liked = [], playlists = [], artists_liked = []):
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.type = type
        self.liked_albums = liked_albums
        self.songs_liked = songs_liked
        self.playlists = playlists
        self.artists_liked = artists_liked
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "type": self.type,
            "liked_albums": self.liked_albums,
            "songs_liked": self.songs_liked,
            "playlists": self.playlists,
            "artists_liked": self.artists_liked            
        }
         
    def __str__(self):
        return f"{self.name}/{self.username} es un {self.type}" 
    
    def like_album(self, album_id):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if album_id not in user['liked_albums']:
                    user['liked_albums'].append(album_id.id)
                break
                
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
            
    def like_song(self, song):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if song.id not in user['songs_liked']:
                    user['songs_liked'].append(song.id)
                    song.like()                    
                break
        
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def like_artist(self, artist_id):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if artist_id not in user['artists_liked']:
                    user['artists_liked'].append(artist_id.id)
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)

    def dislike_album(self, album_id):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if album_id in user['liked_albums']:
                    user['liked_albums'].remove(album_id.id)
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def dislike_song(self, song):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if song.id in user['songs_liked']:
                    user['songs_liked'].remove(song.id)
                    song.dislike()                    
                break
        
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def dislike_artist(self, artist_id):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                if artist_id in user['artists_liked']:
                    user['artists_liked'].remove(artist_id.id)
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)              
    
    def show_albums(self):
        print("     ***Álbumes del Artista:***")
        albums = self.get_albums()
        for album in albums:
            print(album)
            
    def show_songs(self):
        print("     ***Canciones del Artista:***")
        songs = self.get_songs()
        for song in songs:
            print(song)
        
    
    
    def get_albums(self):
        with open("db/albums.json", "r") as file:
            all_albums = json.load(file)

        user_albums = [Album(**album) for album in all_albums if album['artist'] == self.id]
        return user_albums
        
    def get_songs(self):
        albums = self.get_albums()
        songs = []
        for album in albums:
            songs += album.get_songs()
        return songs
    
    def edit_name(self, new_name):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                user['name'] = new_name
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def edit_email(self, new_email):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                user['email'] = new_email
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def edit_username(self, new_username):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
            
        for user in all_users:
            if user['id'] == self.id:
                user['username'] = new_username
                break
            
        with open("db/usuarios.json", "w") as file:
            json.dump(all_users, file, indent=4)
            
    def get_liked_albums(self):
        with open("db/albums.json", "r") as file:
            all_albums = json.load(file)
        
        liked_albums = [Album(**album) for album in all_albums if album['id'] in self.liked_albums]
        return liked_albums
    
    def get_liked_songs(self):
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)
        
        liked_songs = [Cancion(**song) for song in all_songs if song['id'] in self.songs_liked]
        return liked_songs
    
    def get_liked_artists(self):
        with open("db/usuarios.json", "r") as file:
            all_artists = json.load(file)
        
        liked_artists = [Usuario(**artist) for artist in all_artists if artist['id'] in self.artists_liked]
        return liked_artists
    
    def get_playlists(self):
        with open("db/playlists.json", "r") as file:
            all_playlists = json.load(file)
        
        user_playlists = [Playlist(**playlist) for playlist in all_playlists if playlist['creator'] == self.id]
        return user_playlists
    
    def get_amount_likes(self):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
        
        likes = sum([1 for user in all_users if self.id in user['artists_liked']])
        return likes
    
    def verify_if_liked(self, user_id):
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
        
        for user in all_users:
            if user['id'] == user_id.id:
                if self.id in user['artists_liked']:
                    return True
                else:
                    return False         
        
        
    def get_top_songs(self):
        songs = self.get_songs()
        top_songs = sorted(songs, key=lambda x: x.played, reverse=True)
        return top_songs[:10]
    
    def get_total_played(self):
        songs = self.get_songs()
        total_played = sum([song.played for song in songs])
        return total_played

class Album():
    def __init__(self, id, name, description, cover, published, genre, artist, tracklist=[]):
        """
        Crea una instancia de la clase Album.

        Args:
            id (int): El ID del álbum.
            name (str): El nombre del álbum.
            description (str): La descripción del álbum.
            cover (str): La portada del álbum.
            published (str): La fecha de publicación del álbum.
            genre (str): El género del álbum.
            artist (int): El ID del artista del álbum.
            tracklist (list, optional): La lista de canciones del álbum. Por defecto es una lista vacía.
        """
        self.id = id
        self.name = name
        self.description = description
        self.cover = cover
        self.published = published
        self.genre = genre
        self.artist = artist
        self.tracklist = tracklist

    def get_songs(self):
        """
        Obtiene las canciones del álbum.

        Returns:
            list: La lista de objetos Cancion que pertenecen al álbum.
        """
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)

        album_songs = [Cancion(**song) for song in all_songs if song['id'] in self.tracklist]
        return album_songs
    
    def get_total_streams(self):
        """
        Obtiene el total de reproducciones del álbum.

        Returns:
            int: El número total de reproducciones del álbum.
        """
        songs = self.get_songs()
        total_streams = sum([song.played for song in songs])
        return total_streams
    
    def get_artist(self):
        """
        Obtiene el artista del álbum.

        Returns:
            Usuario: El objeto Usuario que es el artista del álbum.
        """
        with open("db/usuarios.json", "r") as file:
            all_artists = json.load(file)
        
        artist = [Usuario(**user) for user in all_artists if user['id'] == self.artist]
        return artist[0]
    
    def get_amount_likes(self):
        """
        Obtiene la cantidad de likes del álbum.

        Returns:
            int: El número de likes del álbum.
        """
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
        
        likes = sum([1 for user in all_users if self.id in user['liked_albums']])
        return likes
    
    def verify_if_liked(self, user_id):
        """
        Verifica si un usuario ha dado like al álbum.

        Args:
            user_id (int): El ID del usuario.

        Returns:
            bool: True si el usuario ha dado like al álbum, False en caso contrario.
        """
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
        
        for user in all_users:
            if user['id'] == user_id.id:
                if self.id in user['liked_albums']:
                    return True
                else:
                    return False
    
    def __str__(self):
        """
        Devuelve una representación en forma de cadena del álbum.

        Returns:
            str: La representación en forma de cadena del álbum.
        """
        string = f"Album: {self.name} - {self.published}"
        for count, song in enumerate(self.get_songs()):
            string += f"\t\n{count+1}. {song}"
        return string
        
    

    


        
class Cancion():
    def __init__(self, id, name, duration, link, played = 0, liked = 0):
        """
        Constructor de la clase Cancion.

        Args:
            id (int): El ID de la canción.
            name (str): El nombre de la canción.
            duration (str): La duración de la canción.
            link (str): El enlace de la canción.
            played (int, optional): El número de veces que se ha reproducido la canción. Por defecto es 0.
            liked (int, optional): El número de veces que se ha marcado la canción como "me gusta". Por defecto es 0.
        """
        self.id = id
        self.name = name
        self.duration = duration
        self.link = link
        self.played = played
        self.liked = liked     
        
    def __str__(self):
        """
        Devuelve una representación en cadena de la canción.

        Returns:
            str: La representación en cadena de la canción.
        """
        return f"{self.name} - {self.duration}"
    
    def get_artist(self):
        """
        Obtiene el artista de la canción.

        Returns:
            Usuario: El objeto Usuario que representa al artista de la canción.
        """
        with open("db/albums.json", "r") as file:
            all_albums = json.load(file)
        
        artist = [Usuario(**album) for album in all_albums if album['id'] == self.album]
        return artist[0]
    
    def get_album(self):
        """
        Obtiene el álbum al que pertenece la canción.

        Returns:
            Album: El objeto Album al que pertenece la canción.
        """
        with open("db/albums.json", "r") as file:
            all_albums = json.load(file)
        
        album = [Album(**album) for album in all_albums if album['id'] == self.album]
        return album[0]
    
    def verify_if_liked(self, user_id):
        """
        Verifica si la canción ha sido marcada como "me gusta" por un usuario específico.

        Args:
            user_id (int): El ID del usuario.

        Returns:
            bool: True si la canción ha sido marcada como "me gusta" por el usuario, False en caso contrario.
        """
        with open("db/usuarios.json", "r") as file:
            all_users = json.load(file)
        
        for user in all_users:
            if user['id'] == user_id.id:
                if self.id in user['songs_liked']:
                    return True
                else:
                    return False
        
    def play(self):
        """
        Incrementa el contador de reproducciones de la canción en 1.
        """
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)

        for song in all_songs:
            if song['id'] == self.id:
                song['played'] += 1
                break

        with open("db/canciones.json", "w") as file:
            json.dump(all_songs, file, indent=4)
            
    
    def like(self):
        """
        Incrementa el contador de "me gusta" de la canción en 1.
        """
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)
            
        for song in all_songs:
            if song['id'] == self.id:
                song['liked'] += 1
                break
            
        with open("db/canciones.json", "w") as file:
            json.dump(all_songs, file, indent=4)
            
    def dislike(self):
        """
        Decrementa el contador de "me gusta" de la canción en 1.
        """
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)
            
        for song in all_songs:
            if song['id'] == self.id:
                song['liked'] -= 1
                break
            
        with open("db/canciones.json", "w") as file:
            json.dump(all_songs, file, indent=4)
            
            
                
                
class Playlist():
    """
    Representa una lista de reproducción con sus atributos y métodos.
    """

    def __init__(self, id, name, description, creator, tracks = []):
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.tracks = tracks
        
    def __str__(self):
        return f"{self.name} - {self.description}"
    
    def get_tracks(self):
        """
        Recupera las canciones asociadas a la lista de reproducción desde un archivo JSON.

        Returns:
            Una lista de objetos de canciones.
        """
        with open("db/canciones.json", "r") as file:
            all_songs = json.load(file)
        
        playlist_tracks = [Cancion(**song) for song in all_songs if song['id'] in self.tracks]
        return playlist_tracks
    
    def show_tracks(self):
        """
        Imprime las canciones de la lista de reproducción.
        """
        print("     ***Canciones de la Playlist:***")
        for count, song in enumerate(self.get_tracks()):
            print(f"{count+1}. {song}")
            
    


                
