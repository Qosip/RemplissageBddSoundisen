import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from downloadmp3 import download_mp3
import os
from cleanstring import clean_string
import key

# Initialiser l'API client Spotify
client_id = key.spotify_key
client_secret = key.spotify_secret_key
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Recherche de l'artiste
artist_name = 'Le Wanksi'  # Remplacez par le nom de l'artiste souhaité
results = sp.search(q=artist_name, type='artist', limit=1)

# Récupérer l'ID Spotify de l'artiste
if len(results['artists']['items']) > 0:
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    print('ID Spotify de l\'artiste {}: {}'.format(artist_name, artist_id))
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

# Récupérer tous les albums de l'artiste
albums = sp.artist_albums(artist_id, album_type='album')
for album in albums['items']:
    album_name = album['name']
    album_id = album['id']
    print('Album:', album_name)

    # Récupérer toutes les pistes de l'album
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        track_name = track['name']
        track_number = track['track_number']
        print('   Track {}: {}'.format(track_number, track_name))
        query = "{}_{}".format(artist_name, track_name)
        download_mp3(query, artist_name, clean_string(album_name))

# Récupérer tous les single de l'artiste
single = sp.artist_albums(artist_id, album_type='single')
for single in single['items']:
    single_name = single['name']
    single_id = single['id']
    print('Single:', single_name)

    # Récupérer toutes les pistes de l'album
    tracks = sp.album_tracks(single_id)
    for track in tracks['items']:
        track_name = track['name']
        track_number = track['track_number']
        print('   Track {}: {}'.format(track_number, track_name))
        query = "{}_{}".format(artist_name, track_name)
        download_mp3(query, artist_name, clean_string(single_name))
