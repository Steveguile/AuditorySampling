import folium
import pyodbc
import os
import branca
from bs4 import BeautifulSoup as soup
import pandas as pd
from folium.plugins import MarkerCluster
import webbrowser
import platform
from shutil import copyfile

# Credit for folium guide goes to https://www.youtube.com/watch?v=4RnU5qKTfYY
# Credit for uk-counties JSON goes to https://github.com/deldersveld/topojson
# Credit for pyodbc assistance goes to StackOverflow users ryguy7272 and Gennon for response on https://stackoverflow.com/questions/33725862/connecting-to-microsoft-sql-server-using-python

# db or csv
read_type = 'csv'


if platform.system() == "Linux":
    directory = '/usr/share/nginx/html/'
    dir_name = ''
else:
    directory = os.path.dirname(__file__)
    dir_name = os.path.dirname(__file__).rsplit("/", 1)[0]

if read_type == 'db':
    connection = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"  # move this probably, ignore for now as web app is least important of this
        "Server=DESKTOP-HH0IP9E\PROJECT;"
        "Database=WebApp;"
        "Trusted_Connection=yes;")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM dbo.Audio')
elif read_type == 'csv':
    input_file = os.path.join(dir_name, "data", "audio_files.csv")
    cursor = pd.read_csv(input_file, header=0)

tooltip = 'Click for audio'

# Default Location
m = folium.Map(location=[52.063, -1.533], zoom_start=8) # Center map to UK
marker_cluster = MarkerCluster().add_to(m)
# County Data for colourful map
county_overlay = os.path.join(dir_name, 'data', 'map_data', 'uk-counties.json')


def add_markers():
    if read_type == 'db':
        for row in cursor:
            audio_html = "<audio controls><source src=../" + row[3].replace("\\", "/") + row[4] + "/"" type=/audio/" + row[4][1:len(row)] + "/""></audio>"
            folium.Marker([row[1], row[2]],
                          popup=audio_html,
                          tooltip=tooltip,
                          icon=folium.Icon(color='red', icon='play'),
                          ).add_to(marker_cluster)
    elif read_type == 'csv':
        for row in cursor.get_values():
            audio_html = "<audio controls><source src=../" + row[3].replace("\\", "/") + row[4] + " type=audio/" + row[4][1:len(row)] + "></audio>"
            folium.Marker([row[1], row[2]],
                          popup=audio_html,
                          tooltip=tooltip,
                          icon=folium.Icon(color='red', icon='play'),
                          ).add_to(marker_cluster)


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


def county_plot():
    folium.TopoJson(open(county_overlay),
                    object_path='objects.GBR_adm2',
                    style_function=style_function
                    ).add_to(m)


def add_stylesheet():
    # Add css to folium generated file <link rel="stylesheet" href="css/style.css"/>
    map_html = soup(open(os.path.join(directory, 'index.html'), 'r'), features="html.parser")
    head = map_html.find('link', {"href":"https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css"}) # Insert as last stylesheet
    stylesheet = map_html.new_tag(name='link')
    stylesheet['rel'] = 'stylesheet'
    stylesheet['href'] = './css/style.css'
    head.insert_after(stylesheet)

    with open(os.path.join(directory, 'index.html'), 'w') as f:
        f.write(str(map_html))


def open_browser():
    url = os.path.join(directory, 'index.html')

    # Credit to Shubham Rajput for answer on https://stackoverflow.com/questions/48056052/webbrowser-get-could-not-locate-runnable-browser?rq=1

    # If initialize.py is run, this will always exist here
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    # print(webbrowser._browsers) nothing registering so just register it myself, as always guaranteed to exist
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    # Open in chrome because chrome is best
    webbrowser.get('chrome').open_new_tab(url)


def main():

    add_markers()
    county_plot()
    m.save(os.path.join(directory, 'index.html'))
    add_stylesheet()

    if platform.system() == "Linux":
        # Everything went downhill when I started modifying code to deploy in linux container
        copyfile(os.path.join(directory, 'index.html'), '/var/www/html/index.html')
    else:
        open_browser()


main()
