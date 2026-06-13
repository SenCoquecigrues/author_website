"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
from . import views

urlpatterns = [
    path('', include('writer.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('archives/', include('archives.urls', namespace='archives')),
    path('coquecigrues/', include('coquecigrues.urls', namespace='coquecigrues')),
    path('gadgets/', include('gadgets.urls', namespace='gadgets:index')),
    path('members/', include('accounts.urls', namespace='members')),
    path("pinytree", views.pine_portfolio),
    path('voiture_noire/', include('voiture_noire.urls', namespace='voiture_noire:index')),
]

handler404 = "core.views.error_404"
handler500 = "core.views.error_500"