![Troll 2](https://raw.githubusercontent.com/abrenaut/mrot/master/screenshot.png)

# Movie Ratings Over Time

Plot the evolution over time of a movie's rating using [The Wayback Machine](https://archive.org/web/).

## Prerequisites 

This project requires Python >= 3.5

## Installing 

To install, simply:
 
    virtualenv /path/to/mrot-venv
    source /path/to/mrot-venv/bin/activate
    pip install mrot
    
To plot the ratings over time of the movie 'Memento':

    mrot "Memento"

## Developing

To download the project:

    git clone https://github.com/abrenaut/mrot.git
    cd mrot
    
To download dependencies:
    
    virtualenv /path/to/mrot-venv
    source /path/to/mrot-venv/bin/activate
    pip install -r requirements.txt

## Features

* Queries [OMDb API](http://omdbapi.com/) to obtain movie information
* Use the [The Wayback Scraper](https://github.com/abrenaut/waybackscraper/) to download imdb archives
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
                            machine (default: 2)
      -d DELTA, --delta DELTA
                            minimum number of days between two ratings (default:
                            365)
      -q, --quiet           don't print progress (default: False)
