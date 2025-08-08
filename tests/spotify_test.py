from platforms.SpotifyPlatform import SpotifyPlatform
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def mock_user_playlists():
    return {
        "items": [
            {"name": "Chill", "id": "p1"},
            {"name": "Focus", "id": "p2"},
        ]
    }


@pytest.fixture
def mock_tracks_items():
    # Minimal shape expected by SpotifyPlatform.songs_dict
    return [
        {
            "track": {
                "name": "Lost",
                "album": {"name": "Lost"},
                "artists": [
                    {"name": "Guest Who"},
                    {"name": "Kate Wild"},
                ],
            }
        }
    ]


@pytest.fixture
def spotify_platform_mocked(mock_user_playlists):
    # Skip real __init__ that touches env and OAuth; inject a mock client
    with patch.object(SpotifyPlatform, "__init__", return_value=None):
        platform = SpotifyPlatform()
        sp_mock = MagicMock()
        platform.sp = sp_mock
        platform.user_id = "user123"

        # Common defaults used across tests
        sp_mock.user_playlists.return_value = mock_user_playlists

        return platform


def test_get_playlists(spotify_platform_mocked, mock_user_playlists):
    result = spotify_platform_mocked.get_playlists()
    expected = [p["name"] for p in mock_user_playlists["items"]]
    assert result == expected
    spotify_platform_mocked.sp.user_playlists.assert_called_once_with(
        "user123", limit=50
    )


def test_songs_dict(spotify_platform_mocked, mock_tracks_items):
    result = spotify_platform_mocked.songs_dict(mock_tracks_items)
    # SpotifyPlatform.songs_dict takes the first artist name only
    expected = {
        "tracks": [
            {"name": "Lost", "artists": "Guest Who", "album": "Lost"}
        ]
    }
    assert result == expected


def test_get_songs_id(spotify_platform_mocked, mock_tracks_items):
    # First transform to the structure expected by get_songs_id
    songs = spotify_platform_mocked.songs_dict(mock_tracks_items)

    # Each track search returns one item with an id
    spotify_platform_mocked.sp.search.return_value = {
        "tracks": {"items": [{"id": "id123"}]}
    }

    ids = spotify_platform_mocked.get_songs_id(songs)
    assert ids == ["id123"]

    # Assert search called with expected args
    args, kwargs = spotify_platform_mocked.sp.search.call_args
    # q may be passed as positional or kw; normalize
    q = kwargs.get("q", args[0] if args else "")
    limit = kwargs.get("limit", args[1] if len(args) > 1 else None)
    assert "Lost" in q and "Guest Who" in q and "Lost" in q
    assert limit == 1


def test_playlist_valid_name_false_when_exists(
    spotify_platform_mocked, mock_user_playlists
):
    assert spotify_platform_mocked.playlist_valid_name("Chill") is False


def test_playlist_valid_name_true_when_new(
    spotify_platform_mocked, mock_user_playlists
):
    assert spotify_platform_mocked.playlist_valid_name("Brand New Playlist") is True
