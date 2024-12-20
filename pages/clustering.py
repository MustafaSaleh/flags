
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import json
from utils import rgb_to_hex
import plotly.express as px

def load_color_data():
    with open('country_colors.json', 'r') as json_file:
        return json.load(json_file)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def main():
    st.title("🎨 Flag Colors Clustering Analysis")
    
    country_colors = load_color_data()
    
    # Extract all colors and their countries
    all_colors = []
    color_countries = []
    for country, data in country_colors.items():
        for color, prop in zip(data['colors'], data['proportions']):
            all_colors.append(hex_to_rgb(color))
            color_countries.append(country)
    
    # Convert to numpy array
    X = np.array(all_colors)
    
    # Clustering controls
    col1, col2 = st.columns(2)
    with col1:
        n_clusters = st.slider("Number of clusters", 2, 10, 5)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    
    # Create 3D scatter plot
    fig = px.scatter_3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        color=[rgb_to_hex(c) for c in X],
        hover_data={"Country": color_countries},
        labels={"x": "Red", "y": "Green", "z": "Blue"},
        title="Flag Colors in RGB Space"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display cluster centers
    st.subheader("Cluster Centers")
    centers = kmeans.cluster_centers_.astype(int)
    
    cols = st.columns(n_clusters)
    for idx, (col, center) in enumerate(zip(cols, centers)):
        hex_color = rgb_to_hex(center)
        col.markdown(
            f'<div style="background-color: {hex_color}; padding: 20px; '
            f'text-align: center; color: white; border-radius: 5px;">'
            f'Cluster {idx+1}<br>{hex_color}</div>',
            unsafe_allow_html=True
        )
    
    # Show countries in each cluster
    st.subheader("Countries by Cluster")
    for cluster_idx in range(n_clusters):
        with st.expander(f"Cluster {cluster_idx + 1}"):
            cluster_mask = cluster_labels == cluster_idx
            cluster_countries = set([color_countries[i] for i in np.where(cluster_mask)[0]])
            st.write(", ".join(sorted(cluster_countries)))

if __name__ == "__main__":
    main()
