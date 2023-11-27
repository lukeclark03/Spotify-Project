from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import math
import os
from sklearn.metrics.pairwise import cosine_similarity
import mplcursors  # Import mplcursors for cursor hover labels
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Import colormap for colors
import matplotlib.font_manager as fm

# given a dictionary of songs and their metadata, apply PCA and return similar tracks
def song_pca(songs_metadata, song_ids, playlist_title='playlist', mode='default', mean=[], n_components=5):
    # Convert song metadata to a matrix (rows as songs, columns as features)
    songs_matrix = np.array(list(songs_metadata.values()))

    # Compute mean and variance to compare found songs, add to matrix/dictionary
    if (mode == 'playlist'):
        mean_features = np.mean(songs_matrix, axis=0)
        mean_features = [float(f'{val:.2f}') for val in mean_features] 
        songs_matrix = np.vstack([mean_features, songs_matrix])

        d_mean_features = {}
        d_mean_features['reference'] = mean_features
        songs_metadata = {**d_mean_features, **songs_metadata}

    # Standardize the data (mean=0, variance=1)
    scaler = StandardScaler()
    songs_std = scaler.fit_transform(songs_matrix)

    # Apply PCA
    if (mode == 'playlist'):
        n_components = math.floor(4*math.log(len(songs_metadata), 10)) #maps the n_components to a value based on the amount of tracks dynamically
        if (n_components > 12):
            n_components = 12

    pca = PCA(n_components)  # Define the number of principal components
    songs_pca = pca.fit_transform(songs_std)

    # Explained variance ratio
    explained_var_ratio = pca.explained_variance_ratio_

    # Calculate colors based on distances from mean and similarity ratios
    cosine_ratio = math.log(n_components, 10) - 0.1
    euclidean_ratio = 1-cosine_ratio
    if (mode == 'playlist'):
        mean = songs_pca[0]
    colors, similarity_scores = calculate_similarities(songs_pca, mean, cosine_ratio, euclidean_ratio)  # Using first point as mean

    # Sort songs by similarity scores
    sorted_indices = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)

    # Retrieve top similar songs
    divisor = 0
    if (mode == 'playlist'):
        divisor = 2
    elif (mode == 'recommend'):
        divisor = 6

    top_similar_indices = sorted_indices[1:int(len(songs_metadata)/divisor)]  # Exclude the reference song itself
    top_similar_songs = [list(songs_metadata.keys())[index] for index in top_similar_indices]
    song_ids = [song_ids[index-1] for index in top_similar_indices]

    # create a pair of songs and ids
    songs_and_ids = {}
    length = math.floor(len(songs_metadata)/2)
    n = 0
    for song_name, song_id in zip(top_similar_songs, song_ids):
        if (n == length):
            break
        songs_and_ids[song_name] = song_id
        n += 1

    if (mode == 'recommend'):
        reference_song_index = 0  # Change this index to your chosen reference song
        reference_song_name = list(songs_metadata.keys())[reference_song_index]
        print(f"\n{playlist_title}:")
        for idx, song_index in enumerate(top_similar_indices):
            print(f"{top_similar_songs[idx]} {similarity_scores[song_index]:.2f}")
        print('\n')

    # Plot 2D representation of the data with colors
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(songs_pca[:, 0], songs_pca[:, 1], c=colors, alpha=1)

    # fonts
    font_paths = [
        'dependencies/HIMALAYA.TTF',
        'dependencies/MINGLIUB.TTC',
        'dependencies/SEGUIEMJ.TTF',
        'dependencies/WINGDING.TTF',
        'dependencies/OPENSE.TTF',
        
    ]
    font_props = [fm.FontProperties(fname=path) for path in font_paths]
    plt.rcParams['font.family'] = ['MS Gothic', 'Arial', 'sans-serif']
    plt.rcParams['font.sans-serif'] = [prop.get_name() for prop in font_props] + plt.rcParams['font.sans-serif']

    # Create labels for annotations
    song_names = list(songs_metadata.keys())
    labels = [f"{song_names[i]}" for i in range(len(song_names))]

    # Use mplcursors to display annotations on hover
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{labels[sel.index]} {similarity_scores[sel.index]:.2f}"))

    plt.title(f"Similarity plot for: {playlist_title}")
    plt.xlabel('D1')
    plt.ylabel('D2')
    plt.show()

    return songs_and_ids, mean, n_components

def calculate_similarities(points, mean, cosine_ratio, euclidean_ratio):
    similarity_scores = [(cosine_ratio * cosine_similarity([mean], [point])[0][0]) +
                         (euclidean_ratio * (1 / (1 + np.linalg.norm(mean - point)))) for point in points]

    # Min-Max scaling to standardize similarity scores to the range of 1 to 100
    max_similarity = max(similarity_scores)
    min_similarity = min(similarity_scores)
    scaled_similarities = [100 * (score - min_similarity) / (max_similarity - min_similarity) if max_similarity != min_similarity else 50 for score in similarity_scores]

    tint_values = [1 - (similarity / 100) for similarity in scaled_similarities]
    colors = [cm.Blues(1 - tint + 0.2) for tint in tint_values]
    return colors, scaled_similarities
