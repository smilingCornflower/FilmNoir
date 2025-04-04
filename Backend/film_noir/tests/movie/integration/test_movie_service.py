from django.test import TestCase
from movie.models import Movie
from common.models.genre import Genre
from common.models.actor import Actor
from common.models.director import Director
from movie.service import MovieService
from movie.value_objects import MovieQueryParamsVo, ActorVo, DirectorVo


class TestMovieService(TestCase):
    def setUp(self):
        self.genre1 = Genre.objects.create(name="drama")
        self.genre2 = Genre.objects.create(name="comedy")

        self.actor1 = Actor.objects.create(name="John", surname="Doe")
        self.actor2 = Actor.objects.create(name="Jane", surname="Smith")

        self.director1 = Director.objects.create(name="Chris", surname="Nolan")
        self.director2 = Director.objects.create(name="Quentin", surname="Tarantino")

        self.movie1 = Movie.objects.create(
            title="Movie 1",
            description="desc",
            year=2000,
            rating=8.0,
            director=self.director1,
            poster="movie1.jpg",
            video=None,
        )
        self.movie1.genres.add(self.genre1)
        self.movie1.actors.add(self.actor1)

        self.movie2 = Movie.objects.create(
            title="Movie 2",
            description="desc",
            year=2010,
            rating=7.0,
            director=self.director2,
            poster="movie2.jpg",
            video=None,
        )
        self.movie2.genres.add(self.genre2)
        self.movie2.actors.add(self.actor2)

    def test_filter_by_years(self):
        params = MovieQueryParamsVo(years=[2000], genres=[], actors=[], directors=[])
        result = MovieService.get(params)
        self.assertQuerySetEqual(result, [self.movie1])

    def test_filter_by_genres(self):
        params = MovieQueryParamsVo(years=[], genres=["comedy"], actors=[], directors=[])
        result = MovieService.get(params)
        self.assertQuerySetEqual(result, [self.movie2])

    def test_filter_by_actors(self):
        params = MovieQueryParamsVo(
            years=[], genres=[], actors=[ActorVo(name="John", surname="Doe")], directors=[]
        )
        result = MovieService.get(params)
        self.assertQuerySetEqual(result, [self.movie1])

    def test_filter_by_multiple_params(self):
        params = MovieQueryParamsVo(
            years=[2010],
            genres=["drama"],
            actors=[ActorVo(name="Jane", surname="Smith")],
            directors=[],
        )
        result = MovieService.get(params)
        self.assertQuerySetEqual(
            sorted(result, key=lambda m: m.title),
            sorted([self.movie1, self.movie2], key=lambda m: m.title),
            transform=lambda x: x
        )

    def test_filter_with_no_matches(self):
        params = MovieQueryParamsVo(years=[1900], genres=["thriller"], actors=[], directors=[])
        result = MovieService.get(params)
        self.assertFalse(result.exists())

    def test_filter_with_empty_params(self):
        params = MovieQueryParamsVo(years=[], genres=[], actors=[], directors=[])
        result = MovieService.get(params)
        self.assertEqual(len(result), 2)
