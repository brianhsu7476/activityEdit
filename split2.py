import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# Function to parse XML and ensure no namespaces are applied
def parse_xml(file_path):
    # Parse the XML as usual
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Remove any namespaces in the root element (if any)
    for elem in root.iter():  # Use iter() instead of getiterator()
        # Strip namespace from tags
        elem.tag = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
        # Remove the 'xmlns' attribute if present
        if 'xmlns' in elem.attrib:
            del elem.attrib['xmlns']

    return tree

# Function to write the XML tree back to a file with exact formatting and structure
def write_to_xml(tree, file_path):
    # First, get the XML string (without any namespaces)
    raw_xml = ET.tostring(tree.getroot(), encoding="utf-8", method="xml").decode("utf-8")
    
    # Now, use minidom to pretty print the raw XML
    dom = minidom.parseString(raw_xml)
    pretty_xml = dom.toprettyxml(indent="  ")

    # Write the formatted XML to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

# Example usage:
# Parse the original XML file and strip any namespaces
tree = parse_xml('Morning_Ride.gpx')
a=tree.find('trk').find('trkseg').findall('trkpt')
timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

# Convert the strings to datetime objects

# Calculate the difference in seconds
for i in a:
	dt1 = datetime.strptime(a[0].find('time').text, timestamp_format)
	dt2 = datetime.strptime(i.find('time').text, timestamp_format)
	time_difference = (dt2 - dt1).total_seconds()
	splitpt1=4*3600+42*60+36
	splitpt2=5*3600+10*60+0
	if time_difference>splitpt1 and time_difference<splitpt2:
		tree.find('trk').find('trkseg').remove(i)
# Write the parsed tree back to XML with the same structure and no namespaces
write_to_xml(tree, 'output.gpx')

