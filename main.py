import streamlit as st
import plotly.graph_objects as go
from utils import get_flag_image, rgb_to_hex, get_country_list
from color_processor import ColorProcessor
import json
from datetime import datetime
import base64
import urllib.parse
import numpy as np
from sklearn.cluster import KMeans

# Page configuration
st.set_page_config(
    page_title="Flag Color Analyzer",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/yourusername/flag-color-analyzer',
        'Report a bug':
        "https://github.com/yourusername/flag-color-analyzer/issues",
        'About':
        "# Flag Color Analyzer\nAnalyze and share flag color palettes!"
    })

# Initialize session state for saved palettes
if 'saved_palettes' not in st.session_state:
    st.session_state.saved_palettes = []


# Function to save country colors to a JSON file
def save_country_colors_to_json(filename='country_colors.json'):
    countries = get_country_list()
    country_colors = {}
    for country_code, country_name in countries.items():
        flag_image = get_flag_image(country_code)
        processor = ColorProcessor(flag_image)
        colors, proportions = processor.extract_colors()
        country_colors[country_name] = {
            'colors': [rgb_to_hex(color) for color in colors],
            'proportions': proportions.tolist()
        }

    with open(filename, 'w') as json_file:
        json.dump(country_colors, json_file, indent=2)

    st.success(f"Saved country colors to {filename}")
    return country_colors


# Add custom CSS
st.markdown("""
    <style>
        .color-box {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 10px;
            border: 1px solid #ddd;
        }
        .saved-palette {
            padding: 10px;
            border: 1px solid #ddd;
            margin: 5px 0;
            border-radius: 5px;
        }
        .share-button {
            display: inline-block;
            padding: 5px 10px;
            margin: 5px;
            border-radius: 5px;
            text-decoration: none;
            color: white;
        }
        .twitter-share { background-color: #1DA1F2; }
        .facebook-share { background-color: #4267B2; }
        .linkedin-share { background-color: #0077b5; }
    </style>
""",
            unsafe_allow_html=True)


def create_color_visualization(colors, proportions, title):
    """Create a pie chart visualization of colors."""
    fig = go.Figure(data=[
        go.Pie(labels=[rgb_to_hex(color) for color in colors],
               values=proportions,
               marker=dict(colors=[rgb_to_hex(color) for color in colors]),
               hovertemplate=
               "Color: %{label}<br>Proportion: %{percent}<extra></extra>",
               textinfo='percent')
    ])

    fig.update_layout(title=title,
                      showlegend=True,
                      height=300,
                      margin=dict(t=30, b=0, l=0, r=0))

    return fig


def save_palette(country_name, colors, proportions):
    """Save current color palette to session state."""
    palette = {
        'country': country_name,
        'colors': [rgb_to_hex(color) for color in colors],
        'proportions': proportions.tolist(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.saved_palettes.append(palette)
    return palette


def export_palettes():
    """Export saved palettes as JSON."""
    if st.session_state.saved_palettes:
        export_data = {
            'palettes': st.session_state.saved_palettes,
            'exported_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(export_data, indent=2)
    return None


def create_share_links(palette):
    """Create social media share links for a palette."""
    # Create a shareable text
    palette_text = f"Check out the colors of the {palette['country']} flag! "
    colors_text = " ".join(palette['colors'])
    share_text = urllib.parse.quote(
        f"{palette_text}\nColors: {colors_text}\n#FlagColors #Vexillology")

    # Base URL (replace with your actual deployed URL)
    base_url = "https://colorflagmix.yourdomain.com"
    # Encode palette data for URL
    palette_data = base64.urlsafe_b64encode(
        json.dumps(palette).encode()).decode()
    share_url = urllib.parse.quote(f"{base_url}?palette={palette_data}")

    # Create social media share links
    twitter_link = f"https://twitter.com/intent/tweet?text={share_text}&url={share_url}"
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    linkedin_link = f"https://www.linkedin.com/sharing/share-offsite/?url={share_url}"

    return {
        'twitter': twitter_link,
        'facebook': facebook_link,
        'linkedin': linkedin_link
    }


def display_share_buttons(share_links):
    """Display social media share buttons."""
    st.markdown(f"""
        <div style="margin: 10px 0;">
            <a href="{share_links['twitter']}" target="_blank" class="share-button twitter-share">
                Share on Twitter
            </a>
            <a href="{share_links['facebook']}" target="_blank" class="share-button facebook-share">
                Share on Facebook
            </a>
            <a href="{share_links['linkedin']}" target="_blank" class="share-button linkedin-share">
                Share on LinkedIn
            </a>
        </div>
    """,
                unsafe_allow_html=True)


def main():
    st.title("🎨 Flag Color Analyzer")
    st.markdown("""
    ## Welcome to Flag Color Analyzer

    The **Flag Color Analyzer** is a web-based tool that allows users to analyze and visualize the color palettes of various country flags. Here's a simple breakdown of how it works:
    1. **Country Selection**: Users can select a country from a dropdown list populated with names and codes of countries.

    2. **Flag Display**: Upon selecting a country, the application fetches and displays the flag image for that country.
    3. **Color Extraction**: The app processes the flag image to extract the prominent colors using a clustering algorithm and displays these colors along with their respective proportions.
    4. **Color Mixing**: Users can see visualizations of how the extracted colors can be mixed together in both weighted and equal amounts.
    5. **Save and Share**: Users can save their preferred color palettes and share them on social media platforms like Twitter, Facebook, and LinkedIn. There's also an option to export all saved palettes as a JSON file.
    6. **Visual Features**: The application has an attractive interface with custom CSS for displaying colors as small boxes, making it easy to see which colors are present in each flag.
    Overall, the **Flag Color Analyzer** provides users with an interactive and engaging way to explore the colors found in national flags, making it useful for designers, educators, or anyone interested in vexillology (the study of flags). Users can also share their findings with others easily.
    """)

    # Check for shared palette in URL using new API
    if 'palette' in st.query_params:
        try:
            shared_palette_data = base64.urlsafe_b64decode(
                st.query_params['palette']).decode()
            shared_palette = json.loads(shared_palette_data)
            st.success(
                f"Viewing shared palette from {shared_palette['country']}")
            # Display shared palette
            colors_html = "".join([
                f'<span class="color-box" style="background-color: {color}"></span>'
                for color in shared_palette['colors']
            ])
            st.markdown(f"<div class='saved-palette'>{colors_html}</div>",
                        unsafe_allow_html=True)
            st.markdown("---")
        except Exception as e:
            st.error("Error loading shared palette")

    # Create sidebar for saved palettes
    with st.sidebar:
        st.header("Saved Palettes")
        if st.button("Export All Palettes"):
            export_data = export_palettes()
            if export_data:
                st.download_button(label="Download Palettes (JSON)",
                                   data=export_data,
                                   file_name="flag_palettes.json",
                                   mime="application/json")

        # Display saved palettes
        for idx, palette in enumerate(st.session_state.saved_palettes):
            with st.container():
                st.markdown(f"### {palette['country']}")
                st.markdown(f"Saved on: {palette['timestamp']}")
                colors_html = "".join([
                    f'<span class="color-box" style="background-color: {color}"></span>'
                    for color in palette['colors']
                ])
                st.markdown(f"<div class='saved-palette'>{colors_html}</div>",
                            unsafe_allow_html=True)

                # Add share buttons for each saved palette
                share_links = create_share_links(palette)
                display_share_buttons(share_links)

                if st.button(f"Remove", key=f"remove_{idx}"):
                    st.session_state.saved_palettes.pop(idx)
                    st.rerun()

    # Country selection
    countries = get_country_list()
    search_term = st.text_input("Search country:", "")

    filtered_countries = {
        code: name
        for code, name in countries.items()
        if search_term.lower() in name.lower()
    }

    selected_country = st.selectbox(
        "Select a country:",
        options=list(filtered_countries.keys()),
        format_func=lambda x: filtered_countries[x])

    if selected_country:
        # Load and display flag
        col1, col2 = st.columns([1, 2])

        with col1:
            flag_image = get_flag_image(selected_country)
            st.image(flag_image,
                     caption=f"Flag of {filtered_countries[selected_country]}")

        # Process colors
        processor = ColorProcessor(flag_image)
        colors, proportions = processor.extract_colors()

        with col2:
            st.subheader("Color Analysis")

            # Display individual colors
            for color, prop in zip(colors, proportions):
                hex_color = rgb_to_hex(color)
                st.markdown(
                    f'<div><span class="color-box" style="background-color: {hex_color}"></span>'
                    f'{hex_color} ({prop:.1%})</div>',
                    unsafe_allow_html=True)

            # Add save palette button
            if st.button("Save This Palette"):
                palette = save_palette(filtered_countries[selected_country],
                                       colors, proportions)
                st.success(
                    "Palette saved! Check the sidebar to view saved palettes.")

                # Show share buttons for the newly saved palette
                share_links = create_share_links(palette)
                st.markdown("### Share this palette")
                display_share_buttons(share_links)

        # Color mixing visualizations
        st.subheader("Color Mixing Visualizations")

        col3, col4 = st.columns(2)

        with col3:
            # Weighted mix visualization
            weighted_mix = processor.get_weighted_mix()
            weighted_hex = rgb_to_hex(weighted_mix)
            st.markdown(
                f"### Weighted Mix\n"
                f'<div style="background-color: {weighted_hex}; padding: 20px; '
                f'text-align: center; color: white; margin: 10px 0;">{weighted_hex}</div>',
                unsafe_allow_html=True)
            st.plotly_chart(create_color_visualization(colors, proportions,
                                                       "Color Proportions"),
                            use_container_width=True)

        with col4:
            # Equal mix visualization
            equal_mix = processor.get_equal_mix()
            equal_hex = rgb_to_hex(equal_mix)
            st.markdown(
                f"### Equal Mix\n"
                f'<div style="background-color: {equal_hex}; padding: 20px; '
                f'text-align: center; color: white; margin: 10px 0;">{equal_hex}</div>',
                unsafe_allow_html=True)
            equal_proportions = [1 / len(colors)] * len(colors)
            st.plotly_chart(create_color_visualization(colors,
                                                       equal_proportions,
                                                       "Equal Distribution"),
                            use_container_width=True)


if __name__ == "__main__":
    main()
