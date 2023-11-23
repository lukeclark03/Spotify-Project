import re
import time, random
from collections import OrderedDict

# Function to get metadata and audio features for a list of searched (song, artist)
def get_song_info(spotify, playlist, batch, mode): # gathers info for the playlist
    start = time.time()
    songs_metadata = {}
    track_info = [] # song name, artists, popularity
    batch_ids = []
    batches_processed = 0
    songs_processed = 0

    # organize playlist

    for song in playlist:

        result = []
        track = []

        if (mode == 'search'):
            search_query = f"track:{song[0]} artist:{song[1]}"
            result = spotify.search(q=search_query, type="track", limit=1)
            track = result['tracks']['items'][0]
        
        else: # mode == playlist
            track = song # results['items']

        if (mode == 'playlist' or result['tracks']['items']):
            # Extract song label
            track_name = track['name']
            artist_names = [artist['name'] for artist in track['artists']]
            artists = ', '.join(artist_names)               
            track_labels = (track_name, artists, track['popularity'])
            track_info.append(track_labels)

            # Extract id to batch
            tokens = re.split(r"[\/]", track['href'])
            track_id = tokens[5]
            batch_ids.append(track_id)
            songs_processed += 1

            if songs_processed % batch == 0 or songs_processed == len(playlist):
                # Get audio features for the track batch
                audio_features = exponential_backoff(get_audio_features, spotify, batch_ids)

                for idx, audio_feature in enumerate(audio_features):
                    # Retrieve the track details within the batch loop
                    idx += batches_processed * batch
                    current_song = f"{track_info[idx][0]} - {track_info[idx][1]}"

                    # Process audio features for each track in the batch
                    feature_data = [
                        track_info[idx][2], # popularity
                        audio_feature['danceability'],
                        audio_feature['energy'],
                        audio_feature['key'],
                        audio_feature['loudness'],
                        audio_feature['speechiness'],
                        audio_feature['acousticness'],
                        audio_feature['instrumentalness'],
                        audio_feature['liveness'],
                        audio_feature['valence'],
                        audio_feature['tempo'],
                        audio_feature['time_signature']
                    ]

                    songs_metadata[current_song] = feature_data 

                batch_ids = []  # Clear batch IDs for next batch
                batches_processed += 1
        
        else:
            print(f"    {song} - {artist} not found!")

        # Update progress every 5 seconds
        current = time.time()
        if current - start > 5:
            print(f"    Processed {songs_processed} songs out of {len(playlist)}")
            start = current

    print(f'{songs_processed} out of {len(playlist)} songs found')
    songs_metadata = OrderedDict(songs_metadata)
    return songs_metadata

def get_playlist_tracks(spotify, playlist_id):
    tracks = []
    results = spotify.playlist_tracks(playlist_id)

    for item in results['items']:
        track = item['track']
        tracks.append(track)
    
    return tracks

# Function to get recommendations for a playlist
def get_track_recommendations(spotify, playlist, playlist_data):
    # preprocess playlist to generate ids, prompts user to sign in
    results = []
    i = 0
    for track in playlist:
        tracks = []
        # returns 20 recommendations in form result for each track
        result = spotify.recommendations(
        seed_tracks=[track], 
        limit=20,
        min_popularity=playlist_data[i][0],
        max_popularity=playlist_data[i][1],

        min_danceability=playlist_data[i][0],
        max_danceability=playlist_data[i][1],

        min_energy=playlist_data[i][0],
        max_energy=playlist_data[i][1],

        min_loudness=playlist_data[i][0],
        max_loudness=playlist_data[i][1],

        min_speechiness=playlist_data[i][0],
        max_speechiness=playlist_data[i][1],

        min_acousticness=playlist_data[i][0],
        max_acousticness=playlist_data[i][1],

        min_instrumentalness=playlist_data[i][0],
        max_instrumentalness=playlist_data[i][1],

        min_liveness=playlist_data[i][0],
        max_liveness=playlist_data[i][1],

        min_valence=playlist_data[i][0],
        max_valence=playlist_data[i][1],

        min_tempo=playlist_data[i][0],
        max_tempo=playlist_data[i][1],
        )

        i += 1

        # r amount = limit
        for r in result:
            tracks.append(r['id'])
        results.append(tracks)
        
    return results

def get_audio_features(spotify, track_ids):
    return spotify.audio_features(track_ids)

# Function to handle exponential backoff for Spotify API rate limits
def exponential_backoff(request_function, *args, **kwargs):
    retries = 0
    while retries < 100:  # Maximum number of retries
        try:
            return request_function(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            wait_time = ((retries + 2) ** retries) + random.uniform(0, 1)  # Exponential backoff formula
            if (wait_time > 300):
                print(f"Rate limited. Retrying in {(wait_time/60):.2f} minutes...")
            else:
                print(f"Rate limited. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            retries += 1

    print(f"Max rate limit reached. Please check back later.")
    exit(1)

def get_sample_metadata():

    # Read the data from the text file
    file_path = 'song_data.txt'  # Replace this with the path to your file
    with open(file_path, 'r') as file:
        data = file.readlines()

    # Initialize the dictionary to store song metadata
    songs_metadata = {}

    # Iterate through the data and populate the dictionary
    for i in range(0, len(data), 2):
        song_name = data[i].strip()
        features = eval(data[i + 1])  # Convert string to list
        songs_metadata[song_name] = features

    return songs_metadata

# Function to retrieve random track IDs to a specified amount
def get_random_track_ids(spotify, num_tracks):
    track_ids = []
    track_info = []
    songs_processed = 0

    while songs_processed < num_tracks:

        results = spotify.search(q="ok", limit=50, offset=offset, type='track')
        tracks = results['tracks']['items']
        
        for track in tracks:
            track_ids.append(track['id'])
            track_name = track['name']
            artist_names = [artist['name'] for artist in track['artists']]
            artists = ', '.join(artist_names)               
            track_labels = (track_name, artists, track['popularity'])
            track_info.append(track_labels)
            if len(track_ids) >= num_tracks:
                break
        
            audio_features = get_audio_features(spotify, track_ids)

        # Loop through both track_info and audio_features using zip
        for track_info_item, audio_feature in zip(track_info, audio_features):
            # Extract track details from track_info
            track_name = track_info_item[0]
            artists = track_info_item[i]

            # Create the current_song string
            current_song = f"{track_name} - {artists}"

            # Process audio features for each track in the batch
            feature_data = [
                track_info_item[2],  # popularity
                audio_feature['danceability'],
                audio_feature['energy'],
                audio_feature['key'],
                audio_feature['loudness'],
                audio_feature['speechiness'],
                audio_feature['acousticness'],
                audio_feature['instrumentalness'],
                audio_feature['liveness'],
                audio_feature['valence'],
                audio_feature['tempo'],
                audio_feature['time_signature']
            ]

            song_data = f"{current_song}\n{feature_data}\n"
            with open("song_data.txt", "a") as file:  # Open file in append mode
                file.write(song_data)

            songs_processed += 1
            # Update progress every 5 seconds
            current = time.time()
            if current - start > 5:
                print(f"Processed {songs_processed} songs")
                start = current
            track_info = []

        track_ids = []