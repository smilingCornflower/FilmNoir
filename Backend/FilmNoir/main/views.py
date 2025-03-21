from django.http import JsonResponse, HttpRequest


def root(request: HttpRequest):
    return JsonResponse({"msg": "Hello World!"}, status=200)
