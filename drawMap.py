import gpxpy
import folium
import sys

# Load GPX file
with open(sys.argv[1], 'r') as gpx_file:
	gpx = gpxpy.parse(gpx_file)

# Create a map
map = folium.Map(location=[23.5, 121], zoom_start=13)  # Replace with your default location

# Extract GPX data
for track in gpx.tracks:
	for segment in track.segments:
		points = [(point.latitude, point.longitude) for point in segment.points]
		folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(map)

# Save map
map.save('map.html')

