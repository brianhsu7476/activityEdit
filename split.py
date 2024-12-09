import gpxpy
import datetime

def split_gpx_preserving_metadata(input_file, output_file_1, output_file_2, split_time):
	# Read the GPX file
	with open(input_file, 'r') as file:
		gpx = gpxpy.parse(file)
	print(gpx)

	# Ensure there's at least one track
	if not gpx.tracks:
		print("No tracks found in the GPX file.")
		return

	# Get the first track and its segment
	track = gpx.tracks[0]
	segment = track.segments[0]
	points = segment.points

	# Find the split index based on the time
	start_time = points[0].time
	if not start_time:
		print("Start time is missing in the GPX data.")
		return

	split_index = None
	for i, point in enumerate(points):
		elapsed_time = point.time - start_time
		if elapsed_time.total_seconds() >= split_time:
			split_index = i
			break

	if split_index is None:
		print("No point found after the specified split time.")
		return

	# Create two new GPX objects and copy metadata
	gpx1 = gpxpy.gpx.GPX()
	gpx2 = gpxpy.gpx.GPX()

	gpx1.name = gpx.name
	gpx2.name = gpx.name

	# Copy the track to both GPX objects
	gpx1_track = gpxpy.gpx.GPXTrack(name=track.name, description=track.description)
	gpx2_track = gpxpy.gpx.GPXTrack(name=track.name, description=track.description)
	gpx1.tracks.append(gpx1_track)
	gpx2.tracks.append(gpx2_track)

	# Split the segment
	gpx1_segment = gpxpy.gpx.GPXTrackSegment(points[:split_index])
	gpx2_segment = gpxpy.gpx.GPXTrackSegment(points[split_index:])
	gpx1_track.segments.append(gpx1_segment)
	gpx2_track.segments.append(gpx2_segment)

	# Write the new GPX files
	with open(output_file_1, 'w') as file1:
		file1.write(gpx1.to_xml())

	with open(output_file_2, 'w') as file2:
		file2.write(gpx2.to_xml())

	print(f"GPX file split into {output_file_1} and {output_file_2}.")

# Usage example
input_file = 'Morning_Ride.gpx'  # Replace with your GPX file
output_file_1 = 'output_part_1.gpx'
output_file_2 = 'output_part_2.gpx'
split_time = 4 * 3600 + 42 * 60 + 37  # Convert 4:42:36 into seconds

split_gpx_preserving_metadata(input_file, output_file_1, output_file_2, split_time)

