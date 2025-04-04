from dataclasses import asdict

from django.http import QueryDict

from common.converters import ScreenContentQueryParamsVoConverter
from common.value_objects import ScreenContentQueryParamsVo
from movie.value_objects import MovieQueryParamsVo


class MovieQueryParamsVoConverter(ScreenContentQueryParamsVoConverter[MovieQueryParamsVo]):
    @classmethod
    def _get_vo_from_query_dict(cls, data: QueryDict) -> MovieQueryParamsVo:
        screen_content_query_params_vo: ScreenContentQueryParamsVo = super()._get_vo_from_query_dict(data)
        return MovieQueryParamsVo(**asdict(screen_content_query_params_vo))

