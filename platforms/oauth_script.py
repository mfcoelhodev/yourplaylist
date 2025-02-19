import sys, os
from ytmusicapi import YTMusic, setup_oauth

client_id = sys.argv[1]
client_secret = sys.argv[2]
script_dir = os.path.dirname(os.path.abspath(__file__))
oauth_file = os.path.join(script_dir, "oauth.json")
try:
    token = setup_oauth(
                    client_id=client_id,
                    client_secret=client_secret,
                    filepath=oauth_file,
                    open_browser=True,
                )
except Exception as e:
            print(f"Error during OAuth process: {str(e)}")
            raise
