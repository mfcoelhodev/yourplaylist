import spotipy
from spotipy.oauth2 import SpotifyOAuth
from platforms.PlatformInterface import PlatformInterface
from dotenv import load_dotenv, find_dotenv
import os

class SpotifyPlatform(PlatformInterface):

    def __init__(self):
        #Carregando variaveis de ambiente
        load_dotenv(find_dotenv())
        CLIENT_ID=os.getenv("SPOT_CLIENT_ID")
        CLIENT_SECRET=os.getenv("SPOT_CLIENT_SECRET")
        REDIRECT_URI=os.getenv("SPOT_REDIRECT_URI")
        #criando objeto spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="user-read-private user-read-email user-library-read user-library-modify playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public",
        ))
        user_info = self.sp.current_user()
        self.user_id = user_info['id']

    
    def get_playlists(self):
        playlists_all = self.sp.user_playlists(self.user_id, limit=50)
        playlists = [playlist['name'] for playlist in playlists_all['items']]
        return playlists

    def get_songs(self, playlist):
        playlist_id = self.get_playlist_id(playlist)
        results = self.sp.user_playlist_tracks(self.user_id, playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        songs = self.songs_dict(tracks)
        return songs 
        
    
    def new_playlist(self, name, songs_ids):
        #checar se playlist tem nome válido
        if not self.playlist_valid_name(name):
            raise ValueError(f"A playlist named {name} already exists")
        
        playlist = self.sp.user_playlist_create(self.user_id, name, public=False)
        playlist_id = playlist['id']
        self.sp.user_playlist_add_tracks(self.user_id, playlist_id, songs_ids)
        return playlist_id


    def add_songs(self, playlist, songs_ids):
        playlist_id = self.get_playlist_id(playlist)
        self.sp.user_playlist_add_tracks(self.user_id, playlist_id, songs_ids)
        

    def remove_songs(self, playlist, songs_ids):
        playlist_id = self.get_playlist_id(playlist)
        self.sp.user_playlist_remove_all_ocurrences_of_tracks(self.user_id, playlist_id, songs_ids)
        
    def get_playlist_id(self, name):
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists['items']:
            if playlist['name'] == name:
                playlist_id = playlist['id']
                return playlist_id
        raise ValueError(f"Playlist named '{name}' not found.")
    
    
    #melhorar acurácia
    def get_songs_id(self,songs):
        search_strings = []
        songs_ids = []
        for track in songs.get("tracks", []):
            search_dump = f"{track['name']} {track['album']} {track['artists']}"
            search_strings.append(search_dump)
        for search in search_strings:
            result = self.sp.search(q=search,limit=1)
            song_id = result["tracks"]["items"][0]["id"]
            songs_ids.append(song_id)
        return songs_ids

    def songs_dict(self,songs):
        transformed_data = {
            "tracks": []
        }
        for song in songs:
            transformed_track = {
                "name": song["track"]["name"],
                "artists": song["track"]["artists"][0]["name"],
                "album": song["track"]["album"]["name"]
            }
            transformed_data["tracks"].append(transformed_track)
        return transformed_data

    
    def get_liked_songs(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        songs = results['items']
        while results['next']:
            results = self.sp.next(results)
            songs.extend(results['items'])
        saved_songs = self.songs_dict(songs)
        return saved_songs

    def playlist_valid_name(self, name):
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists['items']:
            if playlist['name'] == name:
                return False
        return True