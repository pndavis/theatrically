import folium
import json
from shapely.geometry import shape, Point
from bs4 import BeautifulSoup
from folium.plugins import LocateControl, MarkerCluster

# Create the map
MyMap = folium.Map(location=[47.6078, -122.3424], tiles='OpenStreetMap', zoom_start=11, max_zoom=13, control_scale=True)

				#'Theater Name': [(lat, lon), 'theater type', 'website_URL', 'google_maps_directions_URL'],
seattle_theaters = {'AMC Seattle 10': [(47.66175,-122.31811), 'amc', 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-seattle-10', 'google_maps_directions_URL'],
                	'AMC Pacific Place 11': [(47.61315,-122.33553), 'amc', 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-pacific-place-11', 'google_maps_directions_URL'],
                	'Regal Cinemas Thornton Place 14 & IMAX': [(47.70279,-122.32533), 'regal', 'https://www.regmovies.com/theatres/regal-thornton-place-imax/1937', 'google_maps_directions_URL'],
                	}



for theater, details in seattle_theaters.items():
    # Define marker variables
    name = theater
    coordinates = details[0]
    theater_chain = details[1]
    website = details[2]
    directions = details[3]
    insta_post = 'Hiya'

    custom_icon = folium.CustomIcon('./{}.png'.format(theater_chain), icon_size=(35, 35), popup_anchor=(0, -22))
   
    # Define html inside marker pop-up
    theater_html = folium.Html(f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;">{name}</span></p>
    <p style="text-align: center;"><iframe src={insta_post}embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
    <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 17px;">{name} Website</span></a></p>
    <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 17px;">Directions to {name}</span></a></p>
    """, script=True)
    # Create pop-up with html content
    popup = folium.Popup(theater_html, max_width=700)
    # Create marker with custom icon and pop-up.
    custom_marker = folium.Marker(location=coordinates, icon=custom_icon, tooltip=name, popup=popup)
    custom_marker.add_to(MyMap)
# AMC Pacific Place 11
# AMC Alderwood 16
# AMC Woodinville 12
# AMC Oak Tree 6
# Cinerama
# Grand Illusion Cinema
# SIFF
# Northwest Film Forum
# Boeing IMAX at Pacific Science Center


# Create custom icon


# marker1 = folium.Marker(location=[47.66175,-122.31811], icon=amc_icon)
# marker2 = folium.Marker(location=[47.61169,-122.33370], icon=regal_icon)
# marker1.add_to(MyMap)
# marker2.add_to(MyMap)


# Save the map
MyMap.save('MyMap.html')