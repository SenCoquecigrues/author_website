from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('birthdays', views.Birthday.as_view(), name='birthdays'),

]