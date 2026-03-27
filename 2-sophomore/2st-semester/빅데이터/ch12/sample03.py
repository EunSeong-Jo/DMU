import folium

# pip install folium

map = folium.Map(location=[37.50018, 126.8676],zoom_start=16)
# map.show_in_browser()
map.save('./map.html')


