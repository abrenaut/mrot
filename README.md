# Movie Ratings Over Time

Plot the evolution over time of a movie's rating using [The Wayback Machine](https://archive.org/web/).

## Inspiration

This project was inspired by the [Waybackpack](https://github.com/jsvine/waybackpack) project.

## Installing 

To install, simply:
 
    pip install mrot
    
To plot the ratings over time of the movie 'Memento':

    mrot "Memento"

## Developing

To download the project:

    git clone https://github.com/abrenaut/mrot.git
    cd mrot
    
To download dependencies:
    
    python setup.py install

## Features

* Queries [OMDb API](http://omdbapi.com/) to obtain movie information
* Scrape IMDb archives on [The Wayback Machine](https://archive.org/web/) to extract movie ratings
* Plot the ratings using matplotlib
    
## Usage
    
    usage: mrot [-h] [-c CONCURRENCY] [-d DELTA] [-q] movie_name
    
    Show movie ratings over time.
    
    positional arguments:
      movie_name            the name of the movie
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONCURRENCY, --concurrency CONCURRENCY
                            maximum number of concurrent requests to the wayback
                            machine (default: 5)
      -d DELTA, --delta DELTA
                            minimum number of days between two ratings (default:
                            365)
      -q, --quiet           don't print progress (default: False)
