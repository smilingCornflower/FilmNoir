from tests.configure_app import configure

configure()  # noqa: E402

import unittest

from django.http import QueryDict
from rest_framework.exceptions import ParseError

from common.value_objects import ActorVo, DirectorVo
from movie.converters import MovieQueryParamsVoConverter
from movie.value_objects import MovieQueryParamsVo


class TestMovieQueryParamsVoConverter(unittest.TestCase):
    def test_valid_query_dict(self):
        data = QueryDict(mutable=True)
        data.setlist("years", ["2000", "2010"])
        data.setlist("genres", ["comedy", "drama"])
        data.setlist("actors", ["John Doe", "Jane Smith"])
        data.setlist("directors", ["Chris Nolan", "Quentin Tarantino"])

        vo: MovieQueryParamsVo = MovieQueryParamsVoConverter.get_vo_from_query_dict(
            data
        )

        self.assertEqual(vo.years, [2000, 2010])
        self.assertEqual(vo.genres, ["comedy", "drama"])
        self.assertEqual(
            vo.actors,
            [
                ActorVo(name="John", surname="Doe"),
                ActorVo(name="Jane", surname="Smith"),
            ],
        )
        self.assertEqual(
            vo.directors,
            [
                DirectorVo(name="Chris", surname="Nolan"),
                DirectorVo(name="Quentin", surname="Tarantino"),
            ],
        )

    def test_invalid_actor_format(self):
        data = QueryDict(mutable=True)
        data.setlist("actors", ["OnlyName"])

        with self.assertRaises(ParseError):
            MovieQueryParamsVoConverter.get_vo_from_query_dict(data)

    def test_invalid_year_format(self):
        data = QueryDict(mutable=True)
        data.setlist("years", ["not_a_year"])

        with self.assertRaises(ParseError):
            MovieQueryParamsVoConverter.get_vo_from_query_dict(data)


if __name__ == "__main__":
    unittest.main()
