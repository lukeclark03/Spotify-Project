from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import mplcursors  # Import mplcursors for cursor hover labels
import matplotlib.cm as cm  # Import colormap for colors

# given a dictionary of songs and their metadata, apply PCA and return similar tracks
def song_pca(songs_metadata, playlist_title='playlist'):
    # Convert song metadata to a matrix (rows as songs, columns as features)
    songs_matrix = np.array(list(songs_metadata.values()))

    # Create a mean to compare found songs, add to matrix/dictionary
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
    n_components = math.floor(4*math.log(len(songs_metadata), 10)) #maps the n_components to a value based on the amount of tracks dynamically
    if (n_components > 12):
        n_components = 12

    pca = PCA(n_components)  # Define the number of principal components
    songs_pca = pca.fit_transform(songs_std)

    # Explained variance ratio
    explained_var_ratio = pca.explained_variance_ratio_
    print(f"Explained variance ratio: {explained_var_ratio}")

    # Calculate colors based on distances from mean and similarity ratios
    cosine_ratio = 0.7
    euclidean_ratio = 0.3
    colors, similarity_scores = calculate_similarities(songs_pca, songs_pca[0], cosine_ratio, euclidean_ratio)  # Using first point as mean

    # Sort songs by similarity scores
    sorted_indices = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)

    # Retrieve top similar songs
    top_similar_indices = sorted_indices[1:51]  # Exclude the reference song itself
    top_similar_songs = [list(songs_metadata.keys())[index] for index in top_similar_indices]

    reference_song_index = 0  # Change this index to your chosen reference song
    reference_song_name = list(songs_metadata.keys())[reference_song_index]
    print(f"\nTop 50 similar songs to: {reference_song_name}")
    for idx, song_index in enumerate(top_similar_indices):
        print(top_similar_songs[idx], " ", similarity_scores[song_index])
    print('\n')

        # Plot 2D representation of the data with colors
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(songs_pca[:, 0], songs_pca[:, 1], c=colors, alpha=1)

    # Create labels for annotations
    song_names = list(songs_metadata.keys())
    labels = [f"{song_names[i]}" for i in range(len(song_names))]

    # Get the song names
    song_names = list(songs_metadata.keys())

    # Use mplcursors to display annotations on hover
    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{labels[sel.index]} {similarity_scores[sel.index]:.2f}"))

    mean_similarity = np.mean(similarity_scores)
    plt.title(f"Similarity plot for: {playlist_title}")
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.show()


# Calculations for the graph display
def calculate_distances(point, mean):
    return np.linalg.norm(point - mean)

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
