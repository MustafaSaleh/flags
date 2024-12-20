
import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
import json
from utils import rgb_to_hex, mix_colors
import plotly.express as px
import plotly.graph_objects as go

def load_color_data():
    with open('country_colors.json', 'r') as json_file:
        return json.load(json_file)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def main():
    st.title("🎨 Flag Colors Mixing Analysis")
    
    country_colors = load_color_data()
    
    # Calculate mixed colors for each country
    mixed_colors = {}
    for country, data in country_colors.items():
        colors = [hex_to_rgb(color) for color in data['colors']]
        proportions = data['proportions']
        mixed_colors[country] = mix_colors(colors, proportions)
    
    # Convert mixed colors to array for clustering
    countries = list(mixed_colors.keys())
    X = np.array([mixed_colors[country] for country in countries])
    
    # Clustering controls
    col1, col2 = st.columns(2)
    with col1:
        n_clusters = st.slider("Number of clusters", 2, 10, 5)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    
    # Create 3D scatter plot of mixed colors
    fig = px.scatter_3d(
        x=X[:, 0], y=X[:, 1], z=X[:, 2],
        color=[rgb_to_hex(c) for c in X],
        hover_data={"Country": countries},
        labels={"x": "Red", "y": "Green", "z": "Blue"},
        title="Mixed Flag Colors in RGB Space"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display cluster centers with their mixed colors
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
    
    # Show similar color palettes
    st.subheader("Countries with Similar Mixed Colors")
    for cluster_idx in range(n_clusters):
        with st.expander(f"Color Group {cluster_idx + 1}"):
            cluster_countries = [countries[i] for i in np.where(cluster_labels == cluster_idx)[0]]
            
            # Display mixed colors for each country in cluster
            for country in sorted(cluster_countries):
                hex_color = rgb_to_hex(mixed_colors[country])
                st.markdown(
                    f'<div style="display: flex; align-items: center; margin: 5px 0;">'
                    f'<span style="background-color: {hex_color}; width: 20px; height: 20px; '
                    f'display: inline-block; margin-right: 10px;"></span>'
                    f'{country} - {hex_color}</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
