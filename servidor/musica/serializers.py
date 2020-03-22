from django.contrib.auth.models import User, Group
from musica.models import Song, Album, Artist
from rest_framework import serializers


# Tambien copiado del tutorial https://www.django-rest-framework.org/tutorial/quickstart/#project-setup .........
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.HyperlinkedModelSerializer):
    # Obtenemos los datos del audio así: https://stackoverflow.com/a/27851778
    # todo esto solo es necesario para cambiarle el nombre de la bd
    # title = serializers.CharField(read_only=True, source="cancion.titulo")
    # file = serializers.FileField(read_only=True, source="cancion.archivo")
    #
    #

    #album =
    class Meta:
        model = Song
        #album_detail = AlbumSerializer()
        fields = '__all__'#['title', 'file', 'lyrics']
