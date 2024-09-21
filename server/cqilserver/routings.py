from django.urls import re_path
from .consumers import TextGeneratorConsumer

websocket_urlpatterns = [
    re_path(r'generate_text/$', TextGeneratorConsumer.as_asgi())
]