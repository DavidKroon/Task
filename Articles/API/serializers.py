from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from Articles.models import Article,Category, ArticleTest # testing article, don't forget to remove it
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, required=True)

    class Meta:
        model = Article
        fields = "__all__"


class CategoryArticleSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    def get_articles(self ,obj):
        print(obj.id)
        queryset = Article.objects.filter(category=obj.id)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['title', 'articles']





class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        filter_backends = [filters.SearchFilter]
        search_fields = ['username']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


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




