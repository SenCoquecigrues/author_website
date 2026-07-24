from django.urls import path

from . import views

app_name = 'gadgets'

urlpatterns = [
    path("", views.index, name="index"),
    path("ecritoire", views.ecritoire, name="ecritoire")
]