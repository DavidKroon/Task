from rest_framework import routers, serializers, viewsets
from Articles.models import Article
from django.contrib.auth.models import User
from rest_framework import filters

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        filter_backends = [filters.SearchFilter]
        search_fields = ['username']
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']



