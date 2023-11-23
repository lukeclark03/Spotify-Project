from authorize import auth_credentials
from songInfo import get_song_info, get_playlist_tracks, get_random_track_ids, get_sample_metadata, exponential_backoff
from playlists import get_categories, get_songs
from songPCA import song_pca

def main():
  # login
  spotify = auth_credentials()

  playlist = [
      ("blazing in the dark", "GnB Chili"),
      ("let go", "frou frou"),
      ("banana shake", "hus"),
      ("black dog", "arlo parks"),
      ("dark & handsome", "blood orange"),
      ("haruko", "airospace"),
      ("take it back", "blood orange"),
      ("soup", "xaptiox"),
      ("hirathae", "kentenshi"),
      ("e t h e r e a l", "tokyopill"),
      ("final wish", "ooxygen"),
      ("duvet", "boa"),
      ("clairvoyant", "misogi"),
      ("benzo", "blood orange"),
      ("good for you", "blood orange"),
      ("happiness", "blood orange"),
      ("today", "blood orange"),
      ("take your time", "blood orange"),
      ("hope", "blood orange"),
      ("jewelry", "blood orange"),
      ("holy will", "blood orange"),
      ("nappy wonder", "blood orange"),
      ("out of your league", "blood orange"),
      ("miyazaki", "kill bill: the rapper"),
      ("a toshi no aki", "lamp"),
      ("listening for the weather", "bic runga"),
      ("pizza", "oohyo"),
      ("galaxy", "ladies' code"),
      ("windows forever", "playdate"),
      ("let me be with you", "round table featuring nino"),
      ("last train at 25 o'clock", "lamp"),
      ("line", "kim a reum"),
      ("save me", "gnb chili"),
      ("look", "red velvet"),
      ("sora wa gray", "lamp"),
      ("tameiki no yukue", "lamp"),
      ("signs", "iiso"),
      ("pneuma", "eden fm"),
      ("earthbound", "black balloons"),
      ("thin moon", "mayer hawthorne"),
      ("after hours", "the velvet underground"),
      ("what's good", "tyler, the creator"),
      ("mommy", "r.i.p."),
      ("ifhy", "tyler, the creator"),
      ("ptsd", "jpegmafia"),
      ("i know", "girls rituals"),
      ("4am", "girl in red"),
      ("because i'm young arrogant", "machine girl"),
      ("just a girl", "no doubt"),
      ("beyond love", "beach house"),
      ("zombie", "the cranberries"),
      ("sweater weather", "the neighbourhood"),
      ("black sheep", "metric, brie larson"),
      ("on top", "the girl: next door"),
      ("smells like teen spirit", "nirvana"),
      ("bang bang bang bang", "sohodolls"),
      ("nobody", "mitski"),
      ("not allowed", "tv girl"),
      ("a boy is a gun", "tyler, the creator"),
      ("puppet", "tyler, the creator"),
      ("like someone in love", "bjork"),
      ("master of none", "beach house"),
      ("instrumental 3", "florist"),
      ("afterglow", "luna li"),
      ("lovesong", "adele"),
      ("fantastic fantasy", "COLTEMONIKHA"),
      ("dialect", "airospace"),
      ("here we go again", "airospace"),
      ("i feel like killing myself", "airospace"),
      ("heartunderblade", "airospace"),
      ("human", "airospace"),
      ("nimbasa core", "plasterbrain"),
      ("pornhub", "airospace"),
      ("miracle at the meadow", "airospace"),
      ("azalea", "airospace"),
      ("alabama ave se", "airospace"),
      ("cryatnite", "airospace"),

      # Add more songs and artists as needed
  ]

  playlist = []

  # retrieves metadata of playlist
  print("gathering metadata...")
  # songs_metadata = get_sample_metadata()
  # songs_metadata = get_song_info(spotify, playlist, 100, 'search')
  # songs_metadata = get_track_recommendations(spotify, playlist, playlist_data)
  # Replace 'YOUR_PLAYLIST_ID' with the actual ID of the playlist

  playlist_id = 'https://open.spotify.com/playlist/6RmyesszNTppKIUK29ql3e?si=d82c3dadd464482b'  # Extracted ID from the playlist URL
  playlist = get_playlist_tracks(spotify, playlist_id)
  songs_metadata = get_song_info(spotify, playlist, 100, 'playlist')
  

  if songs_metadata:
    print("\nanalyzing data...")
    # apply weight aggregation and PCA analysis
    # cosine_ratio finds songs with similar overall sound
    # euclidean_ratio finds songs with similar musical themes

    # TODO: measure the searching track's deviation from the mean. if above, that feature is more important, if below, that feature is less important
    song_pca(songs_metadata) # n_comp = 4*log(track num) cosine = 0.7, euclidean = 0.3
    # Example usage:
    # Assuming you have a 'songs_metadata' dictionary containing song metadata

if __name__ == "__main__":
  main()