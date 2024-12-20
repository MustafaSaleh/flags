import requests
from PIL import Image
from io import BytesIO
import numpy as np


def get_flag_image(country_code):
    """Fetch flag image from country-flags API."""
    url = f"https://flagcdn.com/w640/{country_code.lower()}.png"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def get_country_list():
    """Return a list of country codes and names."""
    return {
        'US': 'United States',
        'GB': 'United Kingdom',
        'FR': 'France',
        'DE': 'Germany',
        'JP': 'Japan',
        'BR': 'Brazil',
        'IN': 'India',
        'CN': 'China',
        'RU': 'Russia',
        'CA': 'Canada',
        'AU': 'Australia',
        'IT': 'Italy',
        'ES': 'Spain',
        'MX': 'Mexico',
        'ZA': 'South Africa',
        'KR': 'South Korea',
        'NG': 'Nigeria',
        'EG': 'Egypt',
        'SA': 'Saudi Arabia',
        'AR': 'Argentina',
        'TR': 'Turkey',
        'NL': 'Netherlands',
        'SE': 'Sweden',
        'CH': 'Switzerland',
        'NO': 'Norway',
        'FI': 'Finland',
        'DK': 'Denmark',
        'PL': 'Poland',
        'PT': 'Portugal',
        'GR': 'Greece',
        'BE': 'Belgium',
        'AT': 'Austria',
        'TH': 'Thailand',
        'VN': 'Vietnam',
        'MY': 'Malaysia',
        'PH': 'Philippines',
        'SG': 'Singapore',
        'NZ': 'New Zealand',
        'ID': 'Indonesia',
        'IR': 'Iran',
        'PK': 'Pakistan',
        'BD': 'Bangladesh',
        'UA': 'Ukraine',
        'IL': 'Israel',
        'KE': 'Kenya',
        'GH': 'Ghana',
        'TZ': 'Tanzania',
        'CO': 'Colombia',
        'VE': 'Venezuela',
        'CL': 'Chile',
        'PE': 'Peru',
        'CZ': 'Czech Republic',
        'HU': 'Hungary',
        'RO': 'Romania',
        'SK': 'Slovakia',
        'BG': 'Bulgaria',
        'AE': 'United Arab Emirates',
        'QA': 'Qatar',
        'KW': 'Kuwait',
        'OM': 'Oman',
        'BH': 'Bahrain',
        'LK': 'Sri Lanka',
        'MM': 'Myanmar',
        'KH': 'Cambodia',
        'LA': 'Laos',
        'NP': 'Nepal',
        'ZW': 'Zimbabwe',
        'ZM': 'Zambia',
        'MW': 'Malawi',
        'UG': 'Uganda',
        'SD': 'Sudan',
        'DZ': 'Algeria',
        'MA': 'Morocco',
        'TN': 'Tunisia',
        'ET': 'Ethiopia',
        'SN': 'Senegal',
        'CI': 'Ivory Coast',
        'ML': 'Mali',
        'BF': 'Burkina Faso',
        'SL': 'Sierra Leone',
        'GM': 'Gambia',
        'LR': 'Liberia',
        'CM': 'Cameroon',
        'CD': 'Democratic Republic of Congo',
        'AO': 'Angola',
        'MZ': 'Mozambique',
        'BW': 'Botswana',
        'NA': 'Namibia',
        'SZ': 'Eswatini',
        'LS': 'Lesotho',
        'BJ': 'Benin',
        'TG': 'Togo',
        'GA': 'Gabon',
        'GN': 'Guinea',
        'TD': 'Chad',
        'NE': 'Niger',
        'ER': 'Eritrea',
        'SO': 'Somalia',
        'CF': 'Central African Republic',
        'RW': 'Rwanda',
        'BI': 'Burundi',
        'MQ': 'Martinique',
        'GP': 'Guadeloupe',
        'RE': 'Réunion',
    }


def mix_colors(colors, weights=None):
    """Mix colors together with optional weights."""
    if weights is None:
        weights = np.ones(len(colors)) / len(colors)
    # Normalize weights
    weights = np.array(weights) / np.sum(weights)
    # Convert colors to numpy array and mix
    colors_array = np.array(colors)
    mixed_color = np.sum(colors_array * weights[:, np.newaxis], axis=0)
    return tuple(int(round(c)) for c in mixed_color)
