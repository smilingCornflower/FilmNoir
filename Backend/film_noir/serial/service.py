from django.db.models import Q

from serial.models import Serial
from serial.value_objects import SerialQueryParamsVo


class SerialService:
    @staticmethod
    def get(params: SerialQueryParamsVo) -> list[Serial]:
        query = Q()

        if params.years:
            query |= Q(year__in=params.years)
        if params.genres:
            query |= Q(genres__name__in=params.genres)
        if params.actors:
            for actor in params.actors:
                query |= Q(actors__name=actor.name, actors__surname=actor.surname)

        result = list(Serial.objects.filter(query).distinct())

        return result
