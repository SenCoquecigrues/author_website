from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('blog', views.Blog.as_view(), name='blog'),
    path('about', views.about, name='about'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]