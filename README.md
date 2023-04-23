# IMDBTop250-python

This  code was created using Python3.10 and Cinemagoer library: https://imdbpy.readthedocs.io/en/latest/

Code gets top 250 IMDB movies pushes them to SQL database and updates it every week on monday

Also this script can parse movies from SQL database by selected genre and print them out in descending order by IMDB score

Script launch:
```
python3.10 imdb_250.py <Genre>

Eg.:

python3.10 imdb_250.py Drama
```
