from dataclasses import asdict

from django.http import QueryDict

from common.converters import ScreenContentQueryParamsVoConverter
from common.value_objects import ScreenContentQueryParamsVo
from serial.value_objects import SerialQueryParamsVo


class SerialQueryParamsVoConverter(
    ScreenContentQueryParamsVoConverter[SerialQueryParamsVo]
):
    @classmethod
    def _get_vo_from_query_dict(cls, data: QueryDict) -> SerialQueryParamsVo:
        screen_content_query_params_vo: ScreenContentQueryParamsVo = (
            super()._get_vo_from_query_dict(data)
        )
        return SerialQueryParamsVo(**asdict(screen_content_query_params_vo))


