from rest_framework import serializers
from domain.models.director import Director


class DirectorSerializer(serializers.ModelSerializer[Director]):
    class Meta:
        model = Director
        fields = "__all__"
