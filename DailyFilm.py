from datetime import datetime

from tmdbv3api import TMDb, Movie, Discover
import random

from Database import Database
from env import *


class DailyFilm:

    def get_daily_film(self):
        tmdb = TMDb()
        tmdb.api_key = TMDB_API_KEY
        while True:
            movie = self.get_random_movie()
            if movie:
                movie_parsed = self.get_parsed_movie(movie)
                Database.insert_movie(movie.id, 1)
                return movie_parsed

    def get_random_movie(self):
        movie = Movie()
        pages = 2
        movies = self.get_movies_list(pages)
        rand_x = random.randint(0, pages*10-1)
        movie_title = movies[rand_x].obj_name
        m = self.get_movie_from_title(movie, movie_title)
        if not self.is_movie_valid(m):
            return False
        return m

    @staticmethod
    def get_movies_list(pages):
        discover = Discover()
        year = random.randint(1910, 2010)
        movies = list()
        for i in range(pages):
            temp_movie = discover.discover_movies({
                'sort_by': 'popularity.desc',
                'year': year,
                'page': i + 1
            })
            movies.extend(temp_movie)
        return movies

    @staticmethod
    def is_movie_valid(movie):
        return Database.is_movie_in_db(movie.id)

    @staticmethod
    def get_movie_from_title(movie, title):
        search = movie.search(title)
        movie_id = search[0].id
        return movie.details(movie_id)

    def get_parsed_movie(self, m):
        index = self.get_movie_index()
        md_title = self.get_md_title(m.title, m.id, m.release_date, m.poster_path)
        md_overview = self.get_md_overview(m.overview)
        md_directors = self.get_md_crew(m.casts['crew'], ["Director"])
        md_writers = self.get_md_crew(m.casts['crew'], ["Writer", "Screenplay", "Author", "Story", "Novel",
                                                        "Characters"])
        md_cast = self.get_md_cast(m.casts['cast'])
        md_tmdb = "[TMDb](https://www.themoviedb.org/)"
        md_rzb = "[RežisöörBot](https://github.com/manueltrinidad/RezisoorBot)"
        template = f"Daily Film No. {index} |{md_title}\n\n" \
                   f"{md_overview}\n\n" \
                   f"Directed By:\n" \
                   f"{md_directors}\n\n" \
                   f"Written By:\n" \
                   f"{md_writers}\n\n" \
                   f"Cast\n" \
                   f"{md_cast}\n\n" \
                   "----------------\n" \
                   f"Data by {md_tmdb} | GitHub {md_rzb}"
        return template

    @staticmethod
    def get_md_title(title, m_id, release_date, poster_url):
        url = "https://www.themoviedb.org/movie/" + str(m_id)
        poster_url = "https://image.tmdb.org/t/p/w300" + poster_url
        dt = datetime.strptime(release_date, "%Y-%M-%d")
        year = dt.year
        return f"[ ]({poster_url})[{title} ({year})]({url})"

    @staticmethod
    def get_movie_index():
        return Database.get_next_index() + 1

    @staticmethod
    def get_md_overview(overview):
        return overview

    @staticmethod
    def get_md_crew(crew, job):
        md_crew = ""
        known_ids = []
        for p in crew:
            if p['job'] in job and p['id'] not in known_ids:
                url = "https://www.themoviedb.org/person/" + str(p['id'])
                md_crew += f"[{p['name']}]({url})  "
                known_ids.append(p['id'])
        return md_crew

    @staticmethod
    def get_md_cast(cast):
        md_cast = ""
        known_ids = []
        cast_len = 5
        if len(cast) <= 5:
            cast_len = len(cast)

        for p in cast[:cast_len]:
            url = "https://www.themoviedb.org/person/" + str(p['id'])
            md_cast += f"[{p['name']}]({url})  "
            known_ids.append(p['id'])

        return md_cast
