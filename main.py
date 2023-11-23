from authorize import auth_credentials
from songInfo import get_song_info, get_playlist_tracks, get_random_track_ids, get_sample_metadata, exponential_backoff
from playlists import get_categories, get_songs
from songPCA import song_pca

def main():
  # login
  spotify = auth_credentials()
  playlist = []
  
  # retrieves metadata of playlist
  print("gathering metadata...")
  # songs_metadata = get_sample_metadata()
  # songs_metadata = get_song_info(spotify, playlist, 100, 'search')
  # songs_metadata = get_track_recommendations(spotify, playlist, playlist_data)

  # Replace 'YOUR_PLAYLIST_ID' with the link to the spotify playlist
  playlist_id = 'https://open.spotify.com/playlist/60R1CVdZVJtvmYiQydIWTe?si=8326ae40e1394dbb'  # Extracted ID from the playlist URL
  playlist = get_playlist_tracks(spotify, playlist_id)
  songs_metadata = get_song_info(spotify, playlist, 100, 'playlist')
  

  if songs_metadata:
    print("\nanalyzing data...")
    # apply weight aggregation and PCA analysis
    # cosine_ratio finds songs with similar overall sound
    # euclidean_ratio finds songs with similar musical themes

    song_pca(songs_metadata) # n_comp = 4*log(track num) cosine = 0.7, euclidean = 0.3
    # Example usage:
    # Assuming you have a 'songs_metadata' dictionary containing song metadata

if __name__ == "__main__":
  main()
