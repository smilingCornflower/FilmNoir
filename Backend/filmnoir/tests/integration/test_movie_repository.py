from tempfile import NamedTemporaryFile

from django.test import TestCase

from domain.exceptions.media import MovieNotFound
from domain.models.actor import Actor
from domain.models.director import Director
from domain.models.genre import Genre
from domain.models.movie import Movie
from domain.value_objects.common import Id, YearVo, RatingVo
from domain.value_objects.filter import MovieFilter
from infrastructure.repositories.movie import DjMovieReadRepository


class TestDjMovieReadRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre_action = Genre.objects.create(name="action")
        cls.genre_comedy = Genre.objects.create(name="comedy")
        cls.genre_drama = Genre.objects.create(name="drama")

        cls.actor_leo = Actor.objects.create(name="Leonardo", surname="DiCaprio")
        cls.actor_tom = Actor.objects.create(name="Tom", surname="Hanks")
        cls.actor_meryl = Actor.objects.create(name="Meryl", surname="Streep")

        cls.director_nolan = Director.objects.create(name="Christopher", surname="Nolan")
        cls.director_scorsese = Director.objects.create(name="Martin", surname="Scorsese")
        cls.director_spielberg = Director.objects.create(name="Steven", surname="Spielberg")

        poster_file = NamedTemporaryFile(suffix=".jpg").name
        video_file = NamedTemporaryFile(suffix=".mp4").name

        cls.movie1 = Movie.objects.create(
            title="Inception",
            description="A thief who steals corporate secrets...",
            year=2010,
            rating=8.8,
            duration=148,
            poster=poster_file,
            video=video_file
        )
        cls.movie1.genres.add(cls.genre_action)
        cls.movie1.actors.add(cls.actor_leo)
        cls.movie1.directors.add(cls.director_nolan)

        cls.movie2 = Movie.objects.create(
            title="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years...",
            year=1994,
            rating=9.3,
            duration=142,
            poster=poster_file
        )
        cls.movie2.genres.add(cls.genre_drama)
        cls.movie2.actors.add(cls.actor_tom)
        cls.movie2.directors.add(cls.director_spielberg)

        cls.movie3 = Movie.objects.create(
            title="Pulp Fiction",
            description="The lives of two mob hitmen...",
            year=1994,
            rating=8.9,
            duration=154,
            poster=poster_file,
            video=video_file
        )
        cls.movie3.genres.add(cls.genre_action, cls.genre_comedy)
        cls.movie3.actors.add(cls.actor_leo, cls.actor_meryl)
        cls.movie3.directors.add(cls.director_scorsese)

        cls.repository = DjMovieReadRepository()

    def test_get_by_id_existing_movie(self):
        result: Movie = self.repository.get_by_id(Id(1))
        self.assertIsInstance(result, Movie)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, self.movie1.title)

    def test_get_by_id_non_existing_movie(self):
        with self.assertRaises(MovieNotFound):
            self.repository.get_by_id(Id(4))

    def test_gel_all_without_filters(self):
        result: list[Movie] = self.repository.get_all(MovieFilter())
        self.assertEqual(len(result), 3)
        self.assertSetEqual({i.id for i in result}, {1, 2, 3})

    def test_get_all_with_id_filter(self):
        filter_ = MovieFilter()
        filter_.id_ = Id(1)
        result: list[Movie] = self.repository.get_all(filter_)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, self.movie1.title)

    def test_get_all_with_years_filter(self):
        filter_ = MovieFilter()
        filter_.years = [YearVo(1994)]
        result: list[Movie] = self.repository.get_all(filter_)
        self.assertEqual(len(result), 2)
        self.assertSetEqual({i.id for i in result}, {2, 3})

    def test_get_all_with_rating_filters(self):
        # Filter with min rating
        filter_ = MovieFilter()
        filter_.min_rating = RatingVo(9.0)
        result = self.repository.get_all(filter_)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, self.movie2.title)

        # Filter with max rating
        filter_ = MovieFilter()
        filter_.max_rating = RatingVo(8.9)
        result = self.repository.get_all(filter_)
        self.assertEqual(len(result), 2)
        self.assertSetEqual({i.id for i in result}, {1, 3})

    def test_get_all_with_genre_ids_filter(self):
        filter_ = MovieFilter()
        filter_.genre_ids = [Id(self.genre_drama.id), Id(self.genre_comedy.id)]
        result = self.repository.get_all(filter_)
        self.assertEqual(len(result), 2)
        self.assertSetEqual({i.id for i in result}, {2, 3})

    def test_get_all_with_actor_ids_filter(self):
        filter_ = MovieFilter()
        filter_.actor_ids = [Id(self.actor_leo.id)]
        result = self.repository.get_all(filter_)
        self.assertEqual(len(result), 2)
        self.assertSetEqual({i.id for i in result}, {1, 3})

    def test_get_all_with_director_ids_filter(self):
        filter_ = MovieFilter()
        filter_.director_ids = [Id(self.director_nolan.id), Id(self.director_spielberg.id)]
        result = self.repository.get_all(filter_)
        self.assertEqual(len(result), 2)
        self.assertSetEqual({i.id for i in result}, {1, 2})

    def test_get_all_with_combined_filters(self):
        filter_ = MovieFilter()
        filter_.min_year = YearVo(1990)
        filter_.max_year = YearVo(2000)
        filter_.min_rating = RatingVo(8.0)
        filter_.max_rating = RatingVo(9.0)
        filter_.actor_ids = [Id(self.actor_leo.id), Id(self.actor_meryl.id)]
        filter_.genre_ids = [Id(self.genre_action.id), Id(self.genre_comedy.id)]
        filter_.director_ids = [Id(self.director_scorsese.id)]

        results = self.repository.get_all(filter_)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, self.movie3.title)