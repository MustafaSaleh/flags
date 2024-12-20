from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


class ColorProcessor:

    def __init__(self, image):
        # Convert image to RGB mode if it isn't already
        self.image = image.convert('RGB')
        self.colors = None
        self.proportions = None

    def extract_colors(self, n_colors=5):
        """Extract main colors from the image using K-means clustering."""
        # Convert image to numpy array
        img_array = np.array(self.image)
        # Reshape array to 2D, each row is a pixel (R,G,B)
        pixels = img_array.reshape(-1, 3)
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_colors, random_state=42)
        kmeans.fit(pixels)
        # Get colors and their proportions
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        # Calculate proportions
        proportion_count = Counter(labels)
        total_pixels = sum(proportion_count.values())
        proportions = [
            proportion_count[i] / total_pixels for i in range(n_colors)
        ]
        # Sort colors by proportion
        sorted_indices = np.argsort(proportions)[::-1]
        self.colors = colors[sorted_indices]
        self.proportions = np.array(proportions)[sorted_indices]
        # Ignore colors less than 1% and transfer their proportion to the closest color
        for i in range(len(self.proportions)):
            if self.proportions[i] < 0.01:
                closest_index = np.argmin(
                    np.linalg.norm(self.colors - self.colors[i], axis=1))
                self.proportions[closest_index] += self.proportions[i]
                self.proportions[i] = 0  # Set to zero since it's ignored
        # Normalize proportions
        self.proportions /= np.sum(
            self.proportions)  # Ensure proportions sum to 1
        return self.colors[self.proportions > 0], self.proportions[
            self.proportions > 0]  # Return valid colors and proportions

    def get_weighted_mix(self):
        """Calculate weighted mix of colors based on proportions."""
        if self.colors is None or self.proportions is None:
            self.extract_colors()
        mixed_color = np.sum(self.colors * self.proportions[:, np.newaxis],
                             axis=0)
        return tuple(int(round(c)) for c in mixed_color)

    def get_equal_mix(self):
        """Calculate equal mix of colors."""
        if self.colors is None:
            self.extract_colors()

        mixed_color = np.mean(self.colors, axis=0)
        return tuple(int(round(c)) for c in mixed_color)
