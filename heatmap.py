import pandas as pd
import folium
from folium.plugins import HeatMap
from branca.colormap import linear
import numpy as np 

# This file is the output of a previous data processing
df = pd.read_csv('data.csv')
df.dropna(subset=['lat', 'lng', 'sum'], inplace=True)

p99 = df['sum'].quantile(0.99) # To prevent extreme outliers
df['clipped'] = df['sum'].clip(upper=p99)
df['probability'] = df['clipped'].rank(pct=True)

# Create the Base Map
map_center = [df['lat'].mean(), df['lng'].mean()]
m = folium.Map(location=map_center, zoom_start=12, tiles="CartoDB positron")

# Add Layers HeatMap.
heat_data = list(zip(df['lat'], df['lng'], df['clipped']))
HeatMap(heat_data, radius=15).add_to(m)

# Add the clickable (invisible) points on top of the heatmap.
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=3,
        color='transparent',
        fill=True,
        fill_color='transparent',
        fill_opacity=1.0,
        popup=f"Probability : {row['probability']:.4f}<br>Average Occurrences: {row['sum']:.1f}"
    ).add_to(m)

m.save("rs_aid_heatmap.html")