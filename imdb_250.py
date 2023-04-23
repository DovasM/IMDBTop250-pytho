import imdb
import mysql.connector
import datetime
import time
import argparse

from mysql.connector import Error


class ImdbTop250:
    def __init__(self):
        arg = self.get_genre()
        self.genre = arg.genre
        self.imdb_obj = imdb.Cinemagoer()
        try:
            self.mydb = mysql.connector.connect(
                host="localhost", user="root", database="imdb_top250"
            )
            if self.mydb.is_connected():
                self.mycursor = self.mydb.cursor()
                self.top250_movies()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def get_genre(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "genre",
            help="Provide a movie genre",
            default="",
        )
        arg = parser.parse_args()
        return arg

    def top250_movies(self):
        top = self.imdb_obj.get_top250_movies()
        self.mycursor.execute("SHOW TABLES")
        tables = self.mycursor.fetchall()
        if ("movies",) not in tables:
            self.mycursor.execute(
                "CREATE TABLE movies (id INT AUTO_INCREMENT PRIMARY KEY, imdb_id VARCHAR(20), title VARCHAR(255), "
                "rating FLOAT, genres TEXT, last_updated DATE)"
            )

        self.mycursor.execute("TRUNCATE TABLE movies")

        for movie in top:
                imdb_id = movie.getID()
                movie = self.imdb_obj.get_movie(imdb_id)
                title = movie['title']
                rating = movie['rating']
                genres = ", ".join(movie['genres'])
                last_updated = datetime.date.today()
                print(imdb_id, title, rating, genres, last_updated)
                self.mycursor.execute("INSERT INTO movies (imdb_id, title, rating, genres, last_updated) VALUES (%s, %s, %s, %s, %s)",
                                 (imdb_id, title, rating, genres, last_updated))
                self.mydb.commit()                         

    def get_movies_by_genre(self):
        self.mycursor.execute(
            "SELECT title, rating FROM movies WHERE genres LIKE %s ORDER BY rating DESC",
            ("%" + self.genre + "%",),
        )
        movies = self.mycursor.fetchall()
        return movies, self.genre
    
    def run_weekly_update(self):
        while True:
            now = datetime.datetime.now()
            day = now.weekday()
            if day == 0:
                self.top250_movies()
            time.sleep(86400 - time.time() % 86400)
            if now.date() > datetime.date(2023, 12, 31): 
                break


def main():
    imdb_top250 = ImdbTop250()
    movies, genre = imdb_top250.get_movies_by_genre()
    if movies:
        print(f"Top {genre} movies:")
        for movie in movies:
            print(f"Title: {movie[0]}, IMDB Score: {movie[1]}")
    imdb_top250.run_weekly_update()


if __name__ == "__main__":
    try:
        main()
    except:
        from traceback import print_exc
        print_exc()
