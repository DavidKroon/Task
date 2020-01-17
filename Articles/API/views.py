from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Articles.models import Article, Category
from Articles.API.serializers import ArticleSerializer, UserSerializer,UserArticleSerializer,ArticleUserSerializer,NestedUserArticleSerializer, ArticleUserJoinSerializer,MyTokenObtainPairSerializer,CategoryArticleSerializer
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView



# rest for articles ////////////////////////////////////////
class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        print(request.query_params)
        search=''
        date='-'
        if request.query_params:
            if  request.query_params.get('search',None):
                search=request.query_params['search']

            if request.query_params.get('date', None):
                date = request.query_params['date']

            queryset = Article.objects.filter(title__contains=search,created_at__contains=date)
        else:
            queryset = Article.objects.all()
        print(queryset)
        serializer = ArticleSerializer(queryset, many=True)
        data=serializer.data
        return Response(data)

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
        instance = Article.objects.get(pk=pk)
        data = request.data

        print(data)
        serialized = ArticleSerializer(instance=instance, data=data)
        #print(serialized)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=204)
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
    permission_classes = (IsAdminUser,)
    def list(self, request):
        queryset = User.objects.all()
        sertializer = UserArticleSerializer(queryset, many=True)
        return Response(sertializer.data)
    def retrieve(self,request,pk=None):
        print(pk)
        queryset = User.objects.filter(id=pk)
        print(queryset)
        sertializer = UserArticleSerializer(queryset,many=True)
        return Response(sertializer.data)

#REST Get full user for an article
class ArticlesUserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Article.objects.all()   #TEST
        serializer = ArticleUserSerializer(queryset,many=True,context={'request':request})
        return  Response(serializer.data)
    def retrieve(self,request,pk=None):
        print(pk)
        queryset = Article.objects.filter(id=pk)    #TEST
        print(queryset)
        sertializer = ArticleUserSerializer(queryset,many=True,context={'request':request})
        return Response(sertializer.data)


#NestedViewset
class NestedUserArticlesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.order_by('id').all()
        serializer = NestedUserArticleSerializer(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        quertyset=User.objects.filter(id=pk)
        serializer=NestedUserArticleSerializer(quertyset,many=True)
        return Response(serializer.data)


class ArticleUserJoinViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Article.objects.all()
        print(queryset)
        serializer=ArticleUserJoinSerializer(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        quertyset=Article.objects.select_related().filter(id=pk).first()
        serializer=ArticleUserJoinSerializer(quertyset)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CategoriesViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Category.objects.all()
        serializer = CategoryArticleSerializer(queryset,many=True)
        return Response(serializer.data)




