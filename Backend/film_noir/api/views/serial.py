from loguru import logger

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from serial.converters import SerialQueryParamsVoConverter
from serial.models import Serial
from serial.serializer import SerialSerializer
from serial.service import SerialService
from serial.value_objects import SerialQueryParamsVo


class SerialView(APIView):
    # TODO: Add schema
    @staticmethod
    def get(request: Request) -> Response:
        logger.debug(f"request query parameters = {request.query_params}")
        params_vo: SerialQueryParamsVo = (
            SerialQueryParamsVoConverter.get_vo_from_query_dict(request.query_params)
        )
        logger.debug(f"converted parameters value object = {params_vo}")
        serials: list[Serial] = SerialService.get(params_vo)

        logger.info(f"{len(serials)} items found")
        return Response(SerialSerializer(serials, many=True).data)
