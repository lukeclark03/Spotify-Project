import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def auth_credentials():
    # Set up a session
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify
