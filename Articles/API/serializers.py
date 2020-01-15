from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from Articles.models import Article,ArticleTest # testing article, don't forget to remove it
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        filter_backends = [filters.SearchFilter]
        search_fields = ['username']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['password'] = user.password
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        # ...

        return token


class UserArticleSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    print(articles)
    def get_articles(self, obj):
        print(' context: ', self.context)
        queryset = Article.objects.filter(author=obj.id)
        articles = ArticleSerializer(queryset, many=True).data
        return articles

    class Meta:
        model = User
        fields = ['id','username', 'articles']


class ArticleUserSerializer(serializers.ModelSerializer):
    author = UserSerializer()



    class Meta:
        model = Article
        fields = ['title', 'content', 'author']


class NestedUserArticleSerializer(serializers.ModelSerializer):
    print('asdasdasdasdasd')

    articles = ArticleSerializer(many=True, read_only=True)

    print(articles)

    class Meta:
        model = User
        fields = ['id', 'username', 'articles']


class ArticleUserJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


