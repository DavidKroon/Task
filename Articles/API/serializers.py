from rest_framework import routers, serializers, viewsets
from Articles.models import Article
from django.contrib.auth.models import User
from rest_framework import filters

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


class UserArticleSerializer(serializers.ModelSerializer):
    #queryset = Article.objects.all()
    #articles = ArticleSerializer(many=True, read_only=True)
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
    #author = UserSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        print(' context: ',self.context)
        queryset = User.objects.filter(id=obj.author.id)
        user = UserSerializer(queryset,context=self.context,many=True).data
        return user

    class Meta:
        model = Article
        fields = ['title','content','user']




