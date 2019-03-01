import folium
import pyodbc
import os
import branca
import winsound

# Credit for folium guide goes to https://www.youtube.com/watch?v=4RnU5qKTfYY
# Credit for uk-counties JSON goes to https://github.com/deldersveld/topojson
# Credit for pyodbc assistance goes to StackOverflow users ryguy7272 and Gennon for response on https://stackoverflow.com/questions/33725862/connecting-to-microsoft-sql-server-using-python

connection = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"  # move this probably, ignore for now as web app is least important of this
    "Server=DESKTOP-HH0IP9E\PROJECT;"
    "Database=WebApp;"
    "Trusted_Connection=yes;")

cursor = connection.cursor()
cursor.execute('SELECT * FROM dbo.Audio')

tooltip = 'Click for audio'

# Default Location
m = folium.Map(location=[52.063, -1.533], zoom_start=8) # Center map to UK
# County Data for colourful map
county_overlay = os.path.join('data', 'uk-counties.json')


#Add markers
for row in cursor:
    audio_html = "<audio controls><source src=""\"" + row[3] + row[4] + "\""" type=\"audio/" + row[4][1:len(row)] + "\"""></audio>"
    folium.Marker([row[1], row[2]],
                  popup=audio_html,
                  tooltip=tooltip,
                  icon=folium.Icon(color='red', icon='play'),
                  ).add_to(m)


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx colour bits
def style_function(feature): # Don't actually care about the feature
    colour = awful_colour_thing(feature)
    return {
        'fillOpacity': 0.5,
        'weight': 0.3,
        'fillColor': colour
    }

def awful_colour_thing(feature):
    scale = 4000
    colourscale = branca.colormap.linear.YlGnBu_09.scale(0, scale)
    feature_int = sum(bytearray(feature.get('properties').get('NAME_2'), 'utf8'))
    if feature_int * 1.5 < scale: # Completely arbitrary decimal value to look pretty
        feature_int = feature_int * 1.5
    colour = colourscale(feature_int)
    return colour
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


# Add overlay
folium.TopoJson(open(county_overlay),
                object_path='objects.GBR_adm2',
                style_function=style_function
                ).add_to(m)

m.save('incident_map.html')



