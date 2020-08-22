import folium
import pandas

data = pandas.read_csv("./Volcanoes.txt")
lat = list(data["LAT"])
long = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def get_color(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

html = '''
Volcano Name:<br>
<a href="https://www.google.com/search?q={} Volcano" target="_blank">{}</a><br>
Height: {} m.
'''
map = folium.Map(location = [40, -99], zoom_start = 4, tiles = "Stamen Terrain")

fg1 = folium.FeatureGroup(name = "Volcanoes")
for lt, ln, el, n in zip(lat, long, elev, name):
    iframe = folium.IFrame(html = html.format(n, n, el), width = 175, height = 75)
    fg1.add_child(folium.CircleMarker(location = [lt, ln], radius = 7, popup = folium.Popup(iframe),
    color = "grey", fill_color = get_color(el), fill_opacity = 0.6))

fg2 = folium.FeatureGroup(name = "Population Layer")
fg2.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = "utf-8-sig").read(),
style_function = lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
else "orange" if 10000000 <= x["properties"]["POP2005"] <= 20000000
else "red"}))

map.add_child(fg1)
map.add_child(fg2)
map.add_child(folium.LayerControl())
map.save("./Map.html")