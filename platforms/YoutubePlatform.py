from platforms.PlatformInterface import PlatformInterface
import os
from dotenv import load_dotenv
from ytmusicapi import YTMusic, setup_oauth
from ytmusicapi.auth.oauth import OAuthCredentials


class YoutubePlatform(PlatformInterface):
    # def get_oauth(self, client_id, client_secret):
    #     script_dir = os.path.dirname(os.path.abspath(__file__))
    #     oauth_file = os.path.join(script_dir, "oauth.json")

    #     try:
    #         # criando oauth.
    #         token = setup_oauth(
    #             client_id=client_id,
    #             client_secret=client_secret,
    #             filepath=oauth_file,
    #             open_browser=True,
    #         )
    #         return token

    #     except Exception as e:
    #         print(f"Error during OAuth process: {str(e)}")
    #         raise

    # autenticação
    def __init__(self):
        load_dotenv()
        CLIENT_ID = os.getenv("YT_CLIENT_ID")
        CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "oauth.json")
        oauth_credentials = OAuthCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )

        if os.path.exists(file_path):
            self.yt = YTMusic(auth=file_path, oauth_credentials=oauth_credentials)
            # print("Log: Login youtube music foi um sucesso!!!")
        else:
            print("Arquivo 'oauth.json' não encontrado.")
            # self.get_oauth(CLIENT_ID, CLIENT_SECRET)
            # self.yt = YTMusic(auth=file_path, oauth_credentials=oauth_credentials)

    def get_playlists(self):
        playlists_all = self.yt.get_library_playlists()
        playlists = [playlist["title"] for playlist in playlists_all]
        return playlists

    def get_songs(self, playlist):
        playlist_id = self.get_playlist_id(playlist)
        tracks_all = self.yt.get_playlist(playlist_id)
        songs_info = self.songs_dict(tracks_all)
        return songs_info

    def new_playlist(self, name, songs):
        playlist_id = self.yt.create_playlist(
            title=name, description="yourplaylist: new playlist", video_ids=songs
        )
        return playlist_id

    def add_songs(self, playlist, songs):
        playlist_id = self.get_playlist_id(playlist)
        self.yt.add_playlist_items(playlist_id, songs)

    def remove_songs(self, playlist, songs):
        playlist_id = self.get_playlist_id(playlist)
        self.yt.remove_playlist_items(playlist_id, songs)

    def playlist_valid_name(self, name):
        playlists = self.yt.get_library_playlists()
        for playlist in playlists:
            if playlist["title"] == name:
                return False
        return True

    def get_playlist_id(self, name):
        playlists = self.yt.get_library_playlists()
        for playlist in playlists:
            if playlist["title"].lower() == name.lower():
                playlist_id = playlist["playlistId"]
                return playlist_id
        raise ValueError(f"Playlist named '{name}' not found.")

    def get_songs_id(self, songs):
        search_strings = []
        songs_ids = []
        for track in songs.get("tracks", []):
            search_dump = f"{track['name']} {track['album']} {track['artists']}"
            search_strings.append(search_dump)
        for search in search_strings:
            dict_result = self.yt.search(query=search, filter="songs", limit=1)
            songs_ids.append(dict_result[0]["videoId"])
        return songs_ids

    def songs_dict(self, songs):
        transformed_data = {"tracks": []}
        for track_list in [songs.get("tracks", [])]:
            for track in track_list:
                if track["album"] == None:
                    transformed_track = {
                        "name": track["title"],
                        "artists": [artist["name"] for artist in track["artists"]],
                        "album": None,
                    }
                else:
                    transformed_track = {
                        "name": track["title"],
                        "artists": [artist["name"] for artist in track["artists"]],
                        "album": track["album"]["name"],
                    }
                transformed_data["tracks"].append(transformed_track)
        return transformed_data

    def get_liked_songs(self):
        liked_songs = self.yt.get_liked_songs(limit=1)
        liked_songs = self.songs_dict(liked_songs)
        return liked_songs
    
    def playlist_public(self, playlist):
        play_id = self.get_playlist_id(playlist)
        self.yt.edit_playlist(playlistId=play_id, privacyStatus="PUBLIC")

    def playlist_private(self, playlist):
        play_id = self.get_playlist_id(playlist)
        self.yt.edit_playlist(playlistId=play_id, privacyStatus="PRIVATE")

    def get_playlist_url(self, name):
        playlists = self.yt.get_library_playlists()
        for playlist in playlists:
            if playlist['title'] == name:
                play_id = playlist['playlistId']
        return f"https://www.youtube.com/playlist?list={play_id}"
    
    def delete_playlist(self, name):
        play_id = self.get_playlist_id(name)
        self.yt.delete_playlist(play_id)