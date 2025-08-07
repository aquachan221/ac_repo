import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point

# Create a GeoDataFrame with your GPS point
lon, lat = -97.1081, 32.7357
point = Point(lon, lat)
gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")  # WGS84

# Convert to Web Mercator for contextily
gdf = gdf.to_crs(epsg=3857)

# Plot the point
ax = gdf.plot(figsize=(8, 8), color="blue", markersize=100)

# Add basemap tiles
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Clean up plot
ax.set_axis_off()
plt.title("Your Location on Real Map")
plt.show()