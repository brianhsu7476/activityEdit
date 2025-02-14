import gpxpy
import gpxpy.gpx

def merge_gpx_files(file1, file2, output_file):
	# Open and parse the first GPX file
	with open(file1, 'r') as f:
		gpx1 = gpxpy.parse(f)

	# Open and parse the second GPX file
	with open(file2, 'r') as f:
		gpx2 = gpxpy.parse(f)

	# Merge all tracks from the second GPX into the first GPX
	for track in gpx2.tracks:
		gpx1.tracks.append(track)

	# Merge all routes from the second GPX into the first GPX
	for route in gpx2.routes:
		gpx1.routes.append(route)

	# Merge all waypoints from the second GPX into the first GPX
	for waypoint in gpx2.waypoints:
		gpx1.waypoints.append(waypoint)

	# Write the merged GPX content to a new file
	with open(output_file, 'w') as f:
		f.write(gpx1.to_xml())

# Example usage
merge_gpx_files('split2-output.gpx', '午間騎乘.gpx', 'merge-output.gpx')

