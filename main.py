import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from downloadmp3 import download_mp3
import os
from cleanstring import clean_string
import key

# Ouvrir le fichier en mode écriture avec suppression du contenu existant
fichier = open("insertArtistSql.sql", "w")

# Initialiser l'API client Spotify
client_id = key.spotify_key
client_secret = key.spotify_secret_key
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_album_cover(name):
    results = sp.album(name)
    if results:
        cover_url = results['images'][0]['url']
        print(cover_url)
        # Utilisez l'URL de la couverture pour faire ce que vous voulez
    else:
        print("Aucun résultat trouvé pour l'album spécifié")

# Recherche de l'artiste
artist_name = 'Le Wanksi'  # Remplacez par le nom de l'artiste souhaité
results = sp.search(q=artist_name, type='artist', limit=1)

# Récupérer l'ID Spotify de l'artiste
if len(results['artists']['items']) > 0:
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    print('ID Spotify de l\'artiste {}: {}'.format(artist_name, artist_id))

    artist_info = sp.artist(artist_id)
    print(artist_info)
    # Récupérer la pp de l'artiste
    profile_photo = artist_info['images'][0]['url']
    # Récupérer le type d'artiste
    artist_type = artist_info['type']
    # Récupérer le style musical principal (sinon enlever le [0])
    genres = artist_info['genres'][0]

    fichier.write("INSERT INTO artiste (nom, prenom, nom_scene, date_naissance, date_mort, photo, type_artiste, style_musical) VALUES ("+ '"' +artist_name+ '"' +", "+ '"' +artist_name+ '"' +", "+ '"' +artist_name+ '"' +", '2000-01-01', NULL, "+ '"' +profile_photo+ '"' +", "+ '"' +artist_type+ '"' +", "+ '"' +genres+ '"' +");\nSET @id_artiste := LAST_INSERT_ID();\n")
else:
    print('Artiste non trouvé')

reparti = clean_string(artist_name)

if not os.path.exists(reparti):
    # Créez le répertoire
    os.makedirs(reparti)
    print("Répertoire créé :", reparti)
else:
    print("Le répertoire existe déjà :", reparti)
#---------------------------------------------------
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def requestSingleAlbum(artist_id, type):
    albums = sp.artist_albums(artist_id, album_type=type, limit=50)
    print(albums)
    for album in albums['items']:
        album_name = album['name']
        album_id = album['id']
        print('Album:', album_name)
        cover_link = album['images'][0]['url']
        release_date = album['release_date']
        print("Date de parution de l'album : ", release_date)

        fichier.write("INSERT INTO album (titre, date_parution) VALUES ("+ '"' +album_name+ '"' +", "+ '"' +release_date+ '"' +");\nSET @id_album := LAST_INSERT_ID();\n")
        fichier.write("INSERT INTO a_publie (id_album, id_artiste) VALUES (@id_album, @id_artiste);\n")
        # Récupérer toutes les pistes de l'album
        tracks = sp.album_tracks(album_id)
        for track in tracks['items']:
            track_name = track['name']
            track_number = track['track_number']
            print('   Track {}: {}'.format(track_number, track_name))
            query = "{}_{}".format(artist_name, track_name)
            data = download_mp3(query, artist_name, clean_string(album_name))
            fichier.write("INSERT INTO morceau (titre, duree, date_parution, style_musical, emplacement, emplacement_morceau) VALUES ("+ '"' +data["titre"]+ '"' +", "+ '"' +data["duree"]+ '"' +", "+ '"' +release_date+ '"' +", "+ '"' +genres+ '"' +", "+ '"' +album['images'][0]['url']+ '"' +", "+ '"' +data["emplacement_morceau"]+ '"' +");\nSET @id_morceau := LAST_INSERT_ID();\n")
            fichier.write("INSERT INTO album_contient_morceaux (id_album, id_morceau) VALUES (@id_album, @id_morceau);\n")
requestSingleAlbum(artist_id, 'album')
requestSingleAlbum(artist_id, 'single')

fichier.close()

''''
nettoyer chaine nom titre musique pour pas avoir ce caractere ' ou ce caractere  "


-- Insérer l'artiste
INSERT INTO artiste (nom, prenom, nom_scene, date_naissance, date_mort, photo, type_artiste, style_musical)
VALUES ('John', 'Doe', 'John Doe', '1990-01-01', NULL, 'john_doe.jpg', 'Chanteur', 'Pop');

-- Récupérer l'identifiant de l'artiste inséré
SET @id_artiste := LAST_INSERT_ID();

-- Insérer l'album
INSERT INTO album (titre, date_parution)
VALUES ('Album A', '2022-01-01');

-- Récupérer l'identifiant de l'album inséré
SET @id_album := LAST_INSERT_ID();

-- Insérer le morceau
INSERT INTO morceau (titre, duree, date_parution, style_musical, emplacement, emplacement_morceau)
VALUES ('Morceau 1', 180, '2022-01-01', 'emplacement1.mp3', 'emplacement_morceau1.mp3', );


-- Récupérer l'identifiant du morceau inséré
SET @id_morceau := LAST_INSERT_ID();

-- Mettre à jour l'enregistrement de l'album avec l'identifiant du morceau
NON INSERTION AUSSI
UPDATE album
SET id_morceau = @id_morceau
WHERE id_album = @id_album;

INSERT INTO album_contient_morceau (album_id, morceau_id)
VALUES (@id_album, @id_morceau);

-- Mettre à jour l'enregistrement de l'artiste avec l'identifiant de l'album

NON INSERTION AUSSI
UPDATE artiste
SET id_album = @id_album
WHERE id_artiste = @id_artiste;
'''