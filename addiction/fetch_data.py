import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os

# 1. AMR DATA (2026 Estimates)
data = {
    'Division': ['Dhaka', 'Chattogram', 'Rajshahi', 'Khulna', 'Barishal', 'Sylhet', 'Rangpur', 'Mymensingh'],
    'AMR_Rate': [82.5, 75.2, 68.4, 61.9, 54.1, 64.3, 58.0, 66.8] 
}
df_amr = pd.DataFrame(data)

# 2. DOWNLOAD MAP DATA TO A LOCAL FILE
url = "https://raw.githubusercontent.com/wmgeolab/geoBoundaries/main/releaseData/gbOpen/BGD/ADM1/geoBoundaries-BGD-ADM1_simplified.geojson"
local_filename = "bd_map.geojson"

try:
    print("Downloading map data to local storage...")
    r = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    
    # Read the local file
    gdf = gpd.read_file(local_filename)
    
    # 3. CLEANING & MERGING
    name_col = 'shapeName' if 'shapeName' in gdf.columns else 'name'
    name_map = {'Chittagong': 'Chattogram', 'Barisal': 'Barishal'}
    gdf[name_col] = gdf[name_col].replace(name_map)

    merged = gdf.merge(df_amr, left_on=name_col, right_on='Division')

    # 4. PLOTTING
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    merged.plot(
        column='AMR_Rate', cmap='YlOrRd', linewidth=0.6, 
        ax=ax, edgecolor='0.4', legend=True,
        legend_kwds={'label': "Resistance Prevalence (%)", 'orientation': "horizontal", 'pad': 0.02}
    )

    # Add Labels
    for idx, row in merged.iterrows():
        centroid = row['geometry'].centroid
        plt.annotate(
            text=f"{row['Division']}\n{row['AMR_Rate']}%", 
            xy=(centroid.x, centroid.y),
            ha='center', fontsize=9, weight='bold',
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.6, ec='none')
        )

    plt.title('Bangladesh AMR Landscape 2026', fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    print("Map successfully generated!")
    plt.show()

    # Clean up the temporary file
    if os.path.exists(local_filename):
        os.remove(local_filename)

except Exception as e:
    print(f"\n[ERROR]: {e}")
    print("Try running: pip install requests pyogrio fiona")