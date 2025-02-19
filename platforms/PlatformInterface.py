from abc import ABC, abstractmethod

class PlatformInterface(ABC):
    #autenticação
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_playlists(self):
        pass

    @abstractmethod
    def get_songs(self, playlist):
        pass
    
    @abstractmethod
    def new_playlist(self, name, songs):
        pass

    @abstractmethod
    def add_songs(self, playlist, songs):
        pass

    @abstractmethod
    def remove_songs(self, playlist, songs):
        pass

    @abstractmethod
    def playlist_valid_name(self, name):
        pass
    
    @abstractmethod
    def get_playlist_id(self, name):
        pass

    @abstractmethod
    def get_songs_id(self,songs):
        pass

    @abstractmethod
    def songs_dict(self,songs):
        pass

    @abstractmethod
    def get_liked_songs(self):
        pass