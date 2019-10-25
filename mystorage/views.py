from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    #검색
    filter_backends = [SearchFilter] # SearchFilter를 기반으로 filtering을 진행할 것이다.
    search_fields = ('title', 'body') # 어떤 칼럼을 기반으로 검색을 할 것인가 -> 튜플!

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #필터링
    def get_queryset(self): 
        qs = super().get_queryset()

        if self.request.user.is_authenticated: #지금 http 요청을 보낸 user가 인증된 user라면
            qs = qs.filter(author = self.request.user) # 로그인한 유저의 글만 필터링해라
        else:
            qs = qs.none()

        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer



class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    parser_classes = (MultiPartParser, FormParser) # 다양한 media 파일을 인코딩할 수 있도록

    # create 함수를 오버라이딩 해야한다. -> create() = post()
    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_201_CREATED)
        else:
            #유효성 검사를 통과하지 못하면 bad request를 응답한다.
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)