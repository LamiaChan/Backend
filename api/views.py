from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import MangaSerializer, ChapterSerializer, PageSerializer, TagSerializer, UserSerializer, NewsItemSerializer, ShowUserSerializer
from core.models import Manga, Page, Chapter, Tag, NewsItem
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from rest_framework.parsers import FileUploadParser, FormParser
from rest_framework.pagination import PageNumberPagination

 #TODO нужно ограничить добавления манги юзерам без прав или сделать модерацуию

class StandardResultsSetPagination(PageNumberPagination):
    """
    Класс с настройкой пагинации 
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


User = get_user_model()

class GetUserInfo(APIView):
    """
    Класс для работы с юзером
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Метод для получения информации
        """
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Метод для обновления данных
        """
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowUserViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода информации о юзере
    """
    queryset = User.objects.all()
    serializer_class = ShowUserSerializer
    http_method_names = ['get']

class CreateUserAPIView(CreateAPIView):
    """
    Класс для создания юзера
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MangaViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода манги
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    #queryset = Manga.objects.all().order_by('-likes')
    serializer_class = MangaSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Метод для сортировки манги
        """
        queryset = Manga.objects.all()
        
        #filtering by query params
        #ex url: http://localhost:8000/api/v1/manga/?likes=less

        likes = self.request.query_params.get('likes')
        updated = self.request.query_params.get('updated')
        published = self.request.query_params.get('published')
        liked_updated = self.request.query_params.get('liked_updated')
        tag = self.request.query_params.get('tag')
 

        if tag:
            if likes == 'more':
                queryset = Manga.objects.filter(tags__pk=tag).order_by('-likes')
            elif likes == 'less':
                queryset = Manga.objects.filter(tags__pk=tag).order_by('likes')
            else:
                queryset = Manga.objects.filter(tags__pk=tag) 
        else:
            if likes == 'more':
                queryset = Manga.objects.all().order_by('-likes')
            elif likes == 'less':
                queryset = Manga.objects.all().order_by('likes')
            elif published == 'earlier':
                queryset = Manga.objects.all().order_by('-year_of_publish')
            elif published == 'later':
                queryset = Manga.objects.all().order_by('year_of_publish')
            elif updated == 'rather':
                queryset = Manga.objects.all().order_by('-updated')
            elif updated == 'newer':
                queryset = Manga.objects.all().order_by('updated')
            elif liked_updated == 'rather':
                queryset = Manga.objects.all().order_by('likes','-updated')
            elif liked_updated == 'newer':
                queryset = Manga.objects.all().order_by('-likes', 'updated')
        
        return queryset

class NewsItemViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода новостей
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #pagination_class = StandardResultsSetPagination
    queryset = NewsItem.objects.all().order_by('-updated')
    serializer_class = NewsItemSerializer
    #need to refactor
    http_method_names = ['get']


class ChapterViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода глав 
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Chapter.objects.all().order_by('-updated')
    serializer_class = ChapterSerializer

class PageViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода страниц 
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    Класс для вывода тегов
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


