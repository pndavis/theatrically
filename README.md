A web app to find movies playing in your area. I would like to revisit this one day, but I abandoned the project because getting theater data is complicated and expensive. 

Problem: There is no good place to see what movies are playing where and when. Movies that aren't blockbusters can go in and out of theaters without you knowing. Or your favorite film might make it's way back to theaters and you have no idea. 

Fandango has no good way of checking what exactly is playing. It prioritizes theaters that use their ticketing. Atom tends to be better, but also struggles for theaters that don’t use their ticketing. AMC and Regal lock you into their own apps, and even then, they have very poor search functionality 


## Key Features:
* Find movies and showtimes playing in your local theater. Can search in a zip code range and date range.
* List of all local movies playing with abitlity to sort by title, release year, or runtime.
* Robust search feature to narrow down showtimes based on title, theater, showtime details, or premium format.
* Showtime page shows all showtimes in a given area and timeframe with ability to sort by title, theater, or time.
* Mobile responsive.

## Todo
* Have theater page. Easy view of every movie a theater is playing now and into the future
* Spruce up movies page
* Build better distiction between pages. Give users options and understanding to best find the info they need
* Search by director/actor
* Working buy button for tickets
* Switch to something other than sqlite for managing database
* Restore posters
* Search by city, not just zip code
* Pulling additional data from the movie database or IMDB

## Bugs to fix/poor design to improve
* Duplicates for certain movies, but this is an issue with the data feed
* 404 with no explanation if there is no theater in range of zip code
* All the searchbars are confusing, with some needing to submit and the other not
* Search results cleared after search

## Long Term Goals
* Notifications for movies you want to see when they come to theaters, directors you like, and actors you like all when they come to theaters near you in the format you want. Alert when something you want to see is about to leave. Alert when a favorite movie of yours is returning to theaters
* Robust search for premium showings like Dolby, IMAX, 70mm, 35mm, Q&A
* Letterboxd integration (eg get notified when a movie that you rated 5 stars returns to theaters)
* Weekly email telling you what is coming to theaters near you
* Abiliity to set a movie theater as your favorite
* Map of the theaters that are being pulled
