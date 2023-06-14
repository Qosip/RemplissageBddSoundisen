from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
from cleanstring import clean_string
import shutil
from pymediainfo import MediaInfo


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

    #On stocke dès maintenant la durée car ensuite elle est supprimée des données du fichier
    clip_info = MediaInfo.parse(mp4_filename)
    duration_ms = clip_info.tracks[0].duration / 1000
    minutes = int(duration_ms // 60)
    seconds = int(duration_ms % 60)
    strminutes = f"{minutes:02d}"
    strseconds = f"{seconds:02d}"
    print("Durée  : " + strminutes + " : " + strseconds)

    mp3_filename = mp4_filename.replace(".mp4", ".mp3")
    query = query.replace(sousrep + "_", "")
    query2 = clean_string(query)
    sousrep2 = clean_string(sousrep)
    os.rename(mp4_filename, "{}_{}.mp3".format(nomalbumsingle, query2))
    shutil.move("{}_{}.mp3".format(nomalbumsingle, query2), "{}/".format(sousrep2))

    print("Téléchargement terminé. Fichier MP3 enregistré sous le nom :", mp3_filename)

    query = query.replace("_", " ")
    data = {
        "titre": query,
        "duree": strminutes + "." + strseconds,
        "emplacement_morceau": "http://prj-web-cir2-grp-58/assets/music/{}/".format(clean_string(sousrep))+"{}_{}.mp3".format(nomalbumsingle, clean_string(query))
    }
    return data
