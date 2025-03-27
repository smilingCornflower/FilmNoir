from tests.configure_app import configure

configure() # noqa: E402


import unittest
from unittest.mock import MagicMock

from movie.serializer import MovieSerializer


class TestMovieSerializer(unittest.TestCase):
    def setUp(self):
        self.genre1 = MagicMock()
        self.genre1.name = "Action"
        self.genre2 = MagicMock()
        self.genre2.name = "Drama"

        self.actor1 = MagicMock()
        self.actor1.name = "John"
        self.actor1.surname = "Doe"

        self.actor2 = MagicMock()
        self.actor2.name = "Jane"
        self.actor2.surname = "Smith"

        self.director = MagicMock()
        self.director.name = "Christopher"
        self.director.surname = "Nolan"

        self.movie = MagicMock()
        self.movie.id = 1
        self.movie.title = "Inception"
        self.movie.description = "A mind-bending thriller"
        self.movie.year = 2010
        self.movie.rating = 8.8
        self.movie.genres.all.return_value = [self.genre1, self.genre2]
        self.movie.actors.all.return_value = [self.actor1, self.actor2]
        self.movie.director = self.director

    def test_single_movie_serialization(self):
        serializer = MovieSerializer(self.movie)
        data = serializer.data

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Inception")
        self.assertEqual(data["description"], "A mind-bending thriller")
        self.assertEqual(data["year"], 2010)
        self.assertEqual(data["rating"], 8.8)
        self.assertEqual(data["genres"], ["Action", "Drama"])
        self.assertEqual(data["actors"], ["John Doe", "Jane Smith"])
        self.assertEqual(data["director"], "Christopher Nolan")

    def test_multiple_movies_serialization(self):
        movie2 = MagicMock()
        movie2.id = 2
        movie2.title = "Interstellar"
        movie2.description = "Space and time"
        movie2.year = 2014
        movie2.rating = 8.6
        movie2.genres.all.return_value = [self.genre1]
        movie2.actors.all.return_value = [self.actor1]
        movie2.director = self.director

        serializer = MovieSerializer([self.movie, movie2], many=True)
        data = serializer.data

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Inception")
        self.assertEqual(data[1]["title"], "Interstellar")
        self.assertEqual(data[1]["genres"], ["Action"])
        self.assertEqual(data[1]["actors"], ["John Doe"])


if __name__ == "__main__":
    unittest.main()
