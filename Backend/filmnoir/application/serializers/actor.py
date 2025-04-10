from rest_framework import serializers

from domain.models.actor import Actor


class ActorSerializer(serializers.ModelSerializer[Actor]):
    class Meta:
        model = Actor
        fields = "__all__"
