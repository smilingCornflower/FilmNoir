from abc import ABC
from typing import Iterable

from rest_framework import serializers

from common.models.base_content import BaseContent


class BaseContentSerializer(serializers.Serializer[BaseContent | Iterable[BaseContent]]):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()

    genres = serializers.SerializerMethodField()

    poster = serializers.CharField()

    @staticmethod
    def get_genres(obj: BaseContent) -> list[str]:
        return [genre.name for genre in obj.genres.all()]