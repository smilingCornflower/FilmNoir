from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
)

from movie.serializer import MovieSerializer

movie_get_schema = extend_schema(
    summary="Get a list of movies",
    responses=MovieSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="years",
            required=False,
            type=OpenApiTypes.INT,
            many=True,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    name="No specific year",
                    value=[],
                ),
                OpenApiExample(
                    name="One year",
                    value=[2014],
                ),
                OpenApiExample(
                    name="Several years",
                    value=[2014, 1994, 2010],
                ),
            ],
        ),
        OpenApiParameter(
            name="genres",
            required=False,
            type=OpenApiTypes.STR,
            many=True,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    name="No specific genre",
                    value=[],
                ),
                OpenApiExample(
                    name="One genre",
                    value=["фантастика"],
                ),
                OpenApiExample(
                    name="Several genres",
                    value=["фантастика", "драма", "приключения"],
                ),
            ],
        ),
        OpenApiParameter(
            name="actors",
            required=False,
            type=OpenApiTypes.STR,
            many=True,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    name="No specific actor",
                    value=[],
                ),
                OpenApiExample(
                    name="one actor",
                    value=["Мэттью Макконахи"],
                ),
                OpenApiExample(
                    name="several actors",
                    value=["Мэттью Макконахи", "Том Хэнкс"],
                ),
            ],
        ),
    ],
)
