from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from Articles.models import Article,ArticleTest # testing article, don't forget to remove it
from django.contrib.auth.models import User
from rest_framework import filters

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTest
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        filter_backends = [filters.SearchFilter]
        search_fields = ['username']


class UserArticleSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    print(articles)
    def get_articles(self, obj):
        print(' context: ', self.context)
        queryset = Article.objects.filter(author=obj.id).select_related('author')
        articles = ArticleSerializer(queryset,many=True).data
        return articles

    class Meta:
        model = User
        fields = ['id','username', 'articles']


class ArticleUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        print(' context: ',self.context)
        try:
             print('USAO')
             queryset = User.objects.filter(id=obj.author.id).first()
        except AttributeError:
            return None

        if queryset is None:
            return None
        return UserSerializer(queryset, context=self.context).data

    class Meta:
        model = ArticleTest
        fields = ['title','content','user']




