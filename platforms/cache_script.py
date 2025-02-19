from platforms.SpotifyPlatform import SpotifyPlatform

try:
    sp = SpotifyPlatform()
except Exception as e:
            print(f"Error during OAuth process: {str(e)}")
            raise
