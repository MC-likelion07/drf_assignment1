from .models import Essay, Album, Files
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

#serializer는 쿼리셋과 모델 인스턴스와 같은 복잡한 데이터를 json으로 변환하여
# python datatype으로 변환할 수 있다.

class EssaySerializer(serializers.ModelSerializer):
    
    author_name = serializers.ReadOnlyField(source = 'author.username') 
    # author를 자동으로 지정, read-only 

    class Meta:
        model = Essay
        fields = ('pk', 'title', 'body', 'author_name')

class AlbumSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source = 'author.username')
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Album
        fields = ('pk', 'author_name', 'image', 'desc')

class FilesSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source = 'author.username')
    myfile = serializers.FileField(use_url = True)

    class Meta:
        model = Files
        fields = ('pk', 'author_name', 'myfile', 'desc')
