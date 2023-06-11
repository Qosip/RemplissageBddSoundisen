from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
from cleanstring import clean_string
import shutil
from mutagen.mp3 import MP3


def download_mp3(query, sousrep, nomalbumsingle):
    # Effectuer la recherche sur YouTube
    search = VideosSearch(query.replace("_", " ")+" lyric")
    search_results = search.result()["result"]

    # Récupérer la première vidéo de la liste des résultats
    video = search_results[0]

    # Obtenir le lien de la vidéo
    video_url = f"https://www.youtube.com/watch?v={video['id']}"

    # Télécharger la vidéo au format MP4
    yt = YouTube(video_url)
    yt.streams.get_audio_only().download()

    # Renommer la vidéo téléchargée en utilisant le titre de la vidéo
    mp4_filename = yt.streams.filter(only_audio=True)[0].default_filename
    mp3_filename = mp4_filename.replace(".mp4", ".mp3")
    os.rename(mp4_filename, "{}_{}.mp3".format(nomalbumsingle, clean_string(query)))
    shutil.move("{}_{}.mp3".format(nomalbumsingle, clean_string(query)), "{}/".format(clean_string(sousrep)))

    audio = MP3("C:/Users/François/Downloads/Daft_Punk_Instant.mp3")
    length = audio.info.length
    print(length)
    minutes = int(length // 60)
    seconds = int(length % 60)
    strminutes = f"{minutes:02d}"
    strseconds = f"{seconds:02d}"
    print("Durée : " + strminutes + " : " + strseconds)


    print("Téléchargement terminé. Fichier MP3 enregistré sous le nom :", mp3_filename)
