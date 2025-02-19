from fuzzywuzzy import fuzz #talvez considere usar rapidfuzz
from platforms.SpotifyPlatform import SpotifyPlatform
from platforms.YoutubePlatform import YoutubePlatform
import yt_dlp
#devolve o objeto da plataforma escolhida
def get_platform(platform_name):
        
    platform_name = platform_name.lower()

    if platform_name == "spotify":
        return SpotifyPlatform()
    elif platform_name == "youtube":
        return YoutubePlatform()
        
    else: 
        raise ValueError(f"Unsupported platform: {platform_name}."
                        "Supported platforms are 'spotify' and 'youtube'")
#descobre se dois nomes de música são iguais o suficiente
def is_equal(song_a, song_b, threshold=60):
        if fuzz.ratio(song_a.lower(), song_b.lower()) >= threshold:
            return True
        return False
#descobre se um nome parecido o suficiente está presente em uma playlist
def is_song_in_list(song_name, song_list, threshold=80):
        for s in song_list:
            if fuzz.ratio(song_name.lower(), s.lower()) >= threshold:
                return True
        return False

def get_songs_names(tracks):
    songs_names = []
    for track in tracks['tracks']:
        songs_names.append(track['name'])    
    return songs_names
