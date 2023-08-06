from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("artek.images.urls", namespace="artek_images")),
]