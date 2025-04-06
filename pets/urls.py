from django.urls import path
from . import views


urlpatterns = [
  path("", views.pets_index, name="pets index"),
]
