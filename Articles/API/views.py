from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Articles.models import Article
from Articles.API.serializers import ArticleSerializer, UserSerializer,UserArticleSerializer,ArticleUserSerializer
from django.contrib.auth.models import User
from rest_framework import filters


# rest for articles ////////////////////////////////////////
class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        print(request.query_params)
        if request.query_params:
            search = request.query_params['search']
            queryset = Article.objects.filter(title=search)
        else:
            queryset = Article.objects.all()
        print(queryset)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serialized = ArticleSerializer(data=data)
        print(serialized)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    # print(data)
    # print(data['title'])
    # newArticle=Article(5,data['title'],data['content'],data['created_at'],data['updated_at'],data['author'])
    # print (newArticle)
    # newArticle.save()
    # return status.HTTP_201_CREATED
    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset.filter(), pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    def update(self, request, pk=None):
        data = request.data
        print(data)
        serialized = ArticleSerializer(data=data)
        print(serialized)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=201)
        else:
            return Response(serialized._errors, status=400)
    def destroy(self, request, pk=None):
        print(pk)
        article = Article.objects.filter(id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# rest for user //////////////////////////////////////
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username','last_login']  # works, filters username
    print(queryset)
    serializer_class = UserSerializer
    def article(self, request, pk=None, ar_pk=None):
        author = self.get_object()
        articles = Article.objects.filter(author=author.id,id=ar_pk) # user id and article id
        serlializer = ArticleSerializer(articles, many=True)
        return Response(serlializer.data)
    def articles(self, request, pk=None, ar_pk=None):
        author = self.get_object()
        articles = Article.objects.filter(author=author.id) # user id
        serlializer = ArticleSerializer(articles, many=True)
        return Response(serlializer.data)

#REST Get all articles for a user
class UserArticleViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset = User.objects.all()
        sertializer = UserArticleSerializer(queryset, many=True)
        return Response(sertializer.data)
    def retrieve(self,request,pk=None):
        print(pk)
        queryset=User.objects.filter(id=pk)
        print(queryset)
        sertializer=UserArticleSerializer(queryset,many=True)
        return Response(sertializer.data)

#REST Get full user for an article
class ArticlesUserViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Article.objects.all()
        serializer=ArticleUserSerializer(queryset,many=True,context={'request':request})
        return  Response(serializer.data)
    def retrieve(self,request,pk=None):
        print(pk)
        queryset=Article.objects.filter(id=pk)
        print(queryset)
        sertializer=ArticleUserSerializer(queryset,many=True,context={'request':request})
        return Response(sertializer.data)

