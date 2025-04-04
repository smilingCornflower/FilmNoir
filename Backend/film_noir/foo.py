import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_noir.settings")
django.setup()


def add_movie_from_dict(data: dict):
    from movie.models import Movie
    from common.models.director import Director
    from common.models.actor import Actor
    from common.models.genre import Genre

    genre_objs = []
    for g in data["genres"]:
        obj, _ = Genre.objects.get_or_create(name=g)
        genre_objs.append(obj)

    actor_objs = []
    for a in data["actors"]:
        obj, _ = Actor.objects.get_or_create(name=a["name"], surname=a["surname"])
        actor_objs.append(obj)

    director, _ = Director.objects.get_or_create(
        name=data["director"]["name"], surname=data["director"]["surname"]
    )

    movie = Movie.objects.create(
        title=data["title"],
        description=data["description"],
        year=data["year"],
        rating=data["rating"],
        director=director,
        poster=data["poster"],
        video=data.get("video"),
    )

    movie.genres.add(*genre_objs)
    movie.actors.add(*actor_objs)
