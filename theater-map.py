import folium
import json
from shapely.geometry import shape, Point
from bs4 import BeautifulSoup
from folium.plugins import LocateControl, MarkerCluster

# Create the map
theater_map = folium.Map(location=[47.6078, -122.3424], tiles='OpenStreetMap', zoom_start=11, max_zoom=15, min_zoom=10, control_scale=True)

				#'Theater Name': [(lat, lon), 'theater type', 'website_URL', 'google_maps_directions_URL'],
seattle_theaters = {'AMC Seattle 10': [(47.66175,-122.31811), 'amc', 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-seattle-10', 'google_maps_directions_URL', '10'],
                	'AMC Pacific Place 11': [(47.61315,-122.33553), 'amc', 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-pacific-place-11', 'google_maps_directions_URL', '11'],
                	'AMC Alderwood 16': [(47.82743,-122.27549), 'amc', 'https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-alderwood-mall-16', 'google_maps_directions_URL', '16'],
                	'Regal Cinemas Thornton Place 14 & IMAX': [(47.70279,-122.32533), 'regal', 'https://www.regmovies.com/theatres/regal-thornton-place-imax/1937', 'google_maps_directions_URL', '14'],
                	'SIFF Cinema Egyptian': [(47.61509,-122.32173), 'siff', 'https://www.siff.net/siff-cinema/venues/siff-cinema-egyptian', 'google_maps_directions_URL', '1'],
                	'SIFF Film Center': [(47.62312,-122.35319), 'siff', 'https://www.siff.net/siff-cinema/venues/siff-film-center', 'google_maps_directions_URL', '1'],
                	'SIFF Cinema Uptown': [(47.62360,-122.35701), 'siff', 'https://www.siff.net/siff-cinema/venues/siff-cinema-uptown', 'google_maps_directions_URL', '3'],
                	'Grand Illusion Cinema': [(47.66474,-122.31284), 'indie', 'https://grandillusioncinema.org', 'google_maps_directions_URL', '1'],
                	}



for theater, details in seattle_theaters.items():
    # Define marker variables
    name = theater
    coordinates = details[0]
    theater_chain = details[1]
    website = details[2]
    directions = details[3]
    insta_post = 'no'
    num_screens = details[4]

    custom_icon = folium.CustomIcon('./movie_pictures/{}.png'.format(theater_chain), icon_size=(35, 35), popup_anchor=(0, -22))
   
    # Define html inside marker pop-up
    theater_html = folium.Html(f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;">{name}</span></p>
    <p style="text-align: center;"><iframe src='./movie_pictures/FilmCenter.jpg'embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
    <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 17px;">{name} Website</span></a></p>
    <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 17px;">Directions to {name}</span></a></p>
    <p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 17px;">Number of screens: {num_screens}</span></a></p>
    """, script=True)
    # Create pop-up with html content
    popup = folium.Popup(theater_html, max_width=700)
    # Create marker with custom icon and pop-up.
    custom_marker = folium.Marker(location=coordinates, icon=custom_icon, tooltip=name, popup=popup)
    custom_marker.add_to(theater_map)

# AMC Woodinville 12
# AMC Oak Tree 6
# Cinerama
# Northwest Film Forum
# Boeing IMAX at Pacific Science Center

# Add geolocation feature to map.
LocateControl(auto_start=False).add_to(theater_map)

# Save the map
theater_map.save('theater-map.html')
