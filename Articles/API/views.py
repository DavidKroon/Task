from rest_framework import routers, serializers, viewsets,status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Articles.models import Article
from Articles.API.serializers import ArticleSerializer,UserSerializer
from django.contrib.auth.models import User


# rest for articles ////////////////////////////////////////
class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    #article_list = ArticleViewSet.as_view({'get': 'list'})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Article.objects.create_user(**serializer.validated_data)

            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Bad data'
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


#rest for user //////////////////////////////////////
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    print(queryset)
    serializer_class = UserSerializer