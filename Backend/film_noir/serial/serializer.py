from django.db.models import QuerySet
from rest_framework import serializers
from typing import Any
from common.serializer import BaseContentSerializer
from common.value_objects import EpisodeVo
from serial.models import Serial, SerialEpisode
from dataclasses import asdict

class SerialSerializer(BaseContentSerializer):
    actors = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()
    episodes = serializers.SerializerMethodField()

    @staticmethod
    def get_actors(obj: Serial) -> list[str]:
        return [actor.name + " " + actor.surname for actor in obj.actors.all()]

    @staticmethod
    def get_director(obj: Serial) -> str:
        return obj.director.name + " " + obj.director.surname

    @staticmethod
    def get_episodes(obj: Serial) -> list[dict[str, Any]]:
        episodes_vo: list[EpisodeVo] = []
        episodes: QuerySet[SerialEpisode] = obj.episodes.all()

        for episode in episodes:
            episode_vo = EpisodeVo(
                content_id=obj.id,
                episode_number=episode.episode_number,
                episode_path=episode.video.path,
            )
            episodes_vo.append(episode_vo)
        return [asdict(i) for i in episodes_vo]
