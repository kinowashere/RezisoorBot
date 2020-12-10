import sqlite3


class Database:

    @staticmethod
    def db_setup():
        conn = sqlite3.connect('dailyfilm.db')
        tb_movies = """
        CREATE TABLE IF NOT EXISTS movies (
            id INT PRIMARY KEY NOT NULL,
            is_valid BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
        conn.execute(tb_movies)
        conn.close()

    @staticmethod
    def is_movie_in_db(m_id):
        conn = sqlite3.connect('dailyfilm.db')
        query = f"SELECT COUNT(id) FROM movies WHERE id = {m_id} ;"
        cursor = conn.execute(query).fetchone()[0]
        conn.close()
        if cursor > 0:
            return False
        return True

    @staticmethod
    def insert_movie(m_id, is_valid):
        conn = sqlite3.connect('dailyfilm.db')
        query = f"INSERT INTO movies (id, is_valid) VALUES ({m_id}, {is_valid}) ;"
        conn.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def get_next_index():
        conn = sqlite3.connect('dailyfilm.db')
        query = "SELECT COUNT(id) FROM movies ;"
        cursor = conn.execute(query).fetchone()[0]
        conn.close()
        return cursor
