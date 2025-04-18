from django.test import TestCase
from unittest.mock import MagicMock, patch
from domain.models.movie import Movie
from application.dto.movie import MovieDto
from application.converters.response_converters.movie import convert_movie_to_dto, convert_movies_to_dto


class TestMovieConverters(TestCase):
    def setUp(self) -> None:
        self.mock_movie = MagicMock(spec=Movie)
        self.mock_movie.id = 1
        self.mock_movie.title = "Test Movie"
        self.mock_movie.description = "Test Description"
        self.mock_movie.year = 2023
        self.mock_movie.rating = 8.5
        self.mock_movie.duration = 120

        self.mock_movie.poster.url = "/media/posters/test_movie.jpg"
        self.mock_movie.video = MagicMock()
        self.mock_movie.video.url = "/media/videos/test_movie.mp4"

        self.mock_genre = MagicMock()
        self.mock_genre.id = 1
        self.mock_genre.name = "Action"

        self.mock_actor = MagicMock()
        self.mock_actor.id = 1
        self.mock_actor.name = "John"
        self.mock_actor.surname = "Doe"

        self.mock_director = MagicMock()
        self.mock_director.id = 1
        self.mock_director.name = "Jane"
        self.mock_director.surname = "Smith"

        self.mock_movie.genres.all.return_value = [self.mock_genre]
        self.mock_movie.actors.all.return_value = [self.mock_actor]
        self.mock_movie.directors.all.return_value = [self.mock_director]

    def test_convert_movie_to_dto_with_all_fields(self) -> None:
        result = convert_movie_to_dto(self.mock_movie)

        self.assertIsInstance(result, MovieDto)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Test Movie")
        self.assertEqual(result.description, "Test Description")
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.rating, 8.5)
        self.assertEqual(result.duration, 120)
        self.assertEqual(result.poster_url, "/media/posters/test_movie.jpg")
        self.assertEqual(result.video_url, "/media/videos/test_movie.mp4")

        self.assertEqual(len(result.genres), 1)
        self.assertEqual(result.genres[0]["id"], 1)
        self.assertEqual(result.genres[0]["name"], "Action")

        self.assertEqual(len(result.actors), 1)
        self.assertEqual(result.actors[0]["id"], 1)
        self.assertEqual(result.actors[0]["name"], "John")
        self.assertEqual(result.actors[0]["surname"], "Doe")

        self.assertEqual(len(result.directors), 1)
        self.assertEqual(result.directors[0]["id"], 1)
        self.assertEqual(result.directors[0]["name"], "Jane")
        self.assertEqual(result.directors[0]["surname"], "Smith")

    def test_convert_movie_to_dto_without_video(self) -> None:
        self.mock_movie.video = None

        result = convert_movie_to_dto(self.mock_movie)

        self.assertIsNone(result.video_url)

    def test_convert_movie_to_dto_with_empty_relations(self) -> None:
        self.mock_movie.genres.all.return_value = []
        self.mock_movie.actors.all.return_value = []
        self.mock_movie.directors.all.return_value = []

        result = convert_movie_to_dto(self.mock_movie)

        self.assertEqual(len(result.genres), 0)
        self.assertEqual(len(result.actors), 0)
        self.assertEqual(len(result.directors), 0)

    def test_convert_movies_to_dto(self) -> None:
        mock_movie2 = MagicMock(spec=Movie)
        mock_movie2.id = 2
        mock_movie2.title = "Test Movie 2"
        mock_movie2.description = "Test Description 2"
        mock_movie2.year = 2022
        mock_movie2.rating = 7.5
        mock_movie2.duration = 90
        mock_movie2.poster.name = "/media/posters/test_movie2.jpg"
        mock_movie2.video = None
        mock_movie2.genres.all.return_value = []
        mock_movie2.actors.all.return_value = []
        mock_movie2.directors.all.return_value = []

        movies = [self.mock_movie, mock_movie2]
        results = convert_movies_to_dto(movies)  # type: ignore

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[1].id, 2)
        self.assertEqual(results[1].video_url, None)
