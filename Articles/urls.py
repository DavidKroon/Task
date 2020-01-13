"""Task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from Articles.API.views import ArticleViewSet, UserViewSet
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet, basename='articles')
urlpatterns = [
    path('api/', include(router.urls)),  # route
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/users/<int:pk>/articles/<int:ar_pk>/', UserViewSet.as_view(actions={'get': 'article'})),
    path('api/users/<int:pk>/articles', UserViewSet.as_view(actions={'get': 'articles'})),
    path('', schema_view)



]
