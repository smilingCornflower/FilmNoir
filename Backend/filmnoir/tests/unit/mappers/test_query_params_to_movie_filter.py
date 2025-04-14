from django.http import QueryDict
from django.test import TestCase
from application.exceptions.mapping import MappingException
from application.mappers.query_params_to_movie_filter import (
    QueryParamsToMovieFilterMapper,
)
from domain.value_objects.common import Id, RatingVo, YearVo
from domain.value_objects.filter import MovieFilter


class TestQueryParamsToMovieFilterMapper(TestCase):
    def test_empty_query_params(self):
        query_params = QueryDict()
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)

        self.assertIsInstance(result, MovieFilter)
        self.assertIsNone(result.years, None)
        self.assertIsNone(result.min_year, None)
        self.assertIsNone(result.max_year, None)
        self.assertIsNone(result.max_rating, None)
        self.assertIsNone(result.min_rating, None)
        self.assertIsNone(result.genre_ids, None)
        self.assertIsNone(result.actor_ids, None)
        self.assertIsNone(result.director_ids, None)

    def test_id_mapping(self):
        query_params = QueryDict("id=42")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.id_, Id(42))

    def test_years_mapping(self):
        query_params = QueryDict("years=1&years=2&years=3")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.years, [YearVo(1), YearVo(2), YearVo(3)])

    def test_year_range_mapping(self):
        query_params = QueryDict("min_year=0&max_year=10")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.min_year, YearVo(0))
        self.assertEqual(result.max_year, YearVo(10))

    def test_rating_range_mapping(self):
        query_params = QueryDict("min_rating=0&max_rating=10")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.min_rating, RatingVo(0))
        self.assertEqual(result.max_rating, RatingVo(10))

    def test_genre_ids_mapping(self):
        query_params = QueryDict("genre_ids=1&genre_ids=2")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.genre_ids, [Id(1), Id(2)])

    def test_actor_ids_mapping(self):
        query_params = QueryDict("actor_ids=1&actor_ids=2")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.actor_ids, [Id(1), Id(2)])

    def test_director_ids_mapping(self):
        query_params = QueryDict("director_ids=1&director_ids=2")
        result: MovieFilter = QueryParamsToMovieFilterMapper.map(query_params)
        self.assertEqual(result.director_ids, [Id(1), Id(2)])

    def test_invalid_data_mapping(self):
        query_params = QueryDict("id=INVALID")
        with self.assertRaises(MappingException):
            QueryParamsToMovieFilterMapper.map(query_params)
