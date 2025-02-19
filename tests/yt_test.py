from platforms.YoutubePlatform import YoutubePlatform
from unittest.mock import patch
import pytest

"""
methods that need mock data:
- get_playlists() --> get_library_playlists()
- get_songs() --> get_playlist() type 1
- get_liked_songs() --> get_liked_songs() type 1
"""

@pytest.fixture
def mock_get_playlists():
    return [{
    'playlistId': 'PLQwVIlKxHM6rz0fDJVv_0UlXGEWf-bFys',
    'title': 'Playlist title',
    'thumbnails': ['test'],
    'count': 5
}]

@pytest.fixture
def mock_get_playlist_songs():
    return    {
        "id": "PLQwVIlKxHM6qv-o99iX9R85og7IzF9YS_",
        "privacy": "PUBLIC",
        "title": "New EDM This Week 03/13/2020",
        "thumbnails": [...],
        "description": "Weekly r/EDM new release roundup. Created with github.com/sigma67/spotifyplaylist_to_gmusic",
        "author": "sigmatics",
        "year": "2020",
        "duration": "6+ hours",
        "duration_seconds": 52651,
        "trackCount": 237,
        "suggestions": [
            {
                "videoId": "HLCsfOykA94",
                "title": "Mambo (GATTÜSO Remix)",
                "artists": [{
                    "name": "Nikki Vianna",
                    "id": "UCMW5eSIO1moVlIBLQzq4PnQ"
                }],
                "album": {
                "name": "Mambo (GATTÜSO Remix)",
                "id": "MPREb_jLeQJsd7U9w"
                },
                "likeStatus": "LIKE",
                "thumbnails": [...],
                "isAvailable": True,
                "isExplicit": False,
                "duration": "3:32",
                "duration_seconds": 212,
                "setVideoId": "to_be_updated_by_client"
            }
        ],
        "related": [
            {
                "title": "Presenting MYRNE",
                "playlistId": "RDCLAK5uy_mbdO3_xdD4NtU1rWI0OmvRSRZ8NH4uJCM",
                "thumbnails": [...],
                "description": "Playlist • YouTube Music"
            }
        ],
        "tracks": [
            {
            "videoId": "bjGppZKiuFE",
            "title": "Lost",
            "artists": [
                {
                "name": "Guest Who",
                "id": "UCkgCRdnnqWnUeIH7EIc3dBg"
                },
                {
                "name": "Kate Wild",
                "id": "UCwR2l3JfJbvB6aq0RnnJfWg"
                }
            ],
            "album": {
                "name": "Lost",
                "id": "MPREb_PxmzvDuqOnC"
            },
            "duration": "2:58",
            "duration_seconds": 178,
            "setVideoId": "748EE8...",
            "likeStatus": "INDIFFERENT",
            "thumbnails": [...],
            "isAvailable": True,
            "isExplicit": False,
            "videoType": "MUSIC_VIDEO_TYPE_OMV",
            "feedbackTokens": {
                "add": "AB9zfpJxtvrU...",
                "remove": "AB9zfpKTyZ..."
                }
            }
        ]
        }

@pytest.fixture
def youtube_platform_mocked(mock_get_playlist_songs, mock_get_playlists):
    # pulando metodo init
    with patch.object(YoutubePlatform, "__init__", return_value=None):
        platform = YoutubePlatform()
        
        with patch("ytmusicapi.YTMusic") as MockYTMusic:
            yt_mock = MockYTMusic.return_value
            
            yt_mock.get_library_playlists.return_value = mock_get_playlists
            yt_mock.get_playlist.return_value = mock_get_playlist_songs
            yt_mock.get_liked_songs.return_value = mock_get_playlist_songs
            
            platform.yt = yt_mock
            return platform

def test_get_playlists(youtube_platform_mocked, mock_get_playlists):
    result = youtube_platform_mocked.get_playlists()
    expected = [playlist["title"] for playlist in mock_get_playlists]
    assert result == expected
    youtube_platform_mocked.yt.get_library_playlists.assert_called_once()

def test_get_liked_songs(youtube_platform_mocked, mock_get_playlist_songs):
    result = youtube_platform_mocked.songs_dict(mock_get_playlist_songs)
    expected = {'tracks': [{'name': 'Lost', 'artists': ['Guest Who', 'Kate Wild'], 'album': 'Lost'}]}
    assert result == expected
    
