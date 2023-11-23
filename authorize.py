import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def auth_credentials():
    # Set up a session
    client_id = "42428055168046b88eb2239b315107a0"
    client_secret = "c7e6feb543d944c09bf5cbf58149b04e"
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify