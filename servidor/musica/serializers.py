from django.contrib.auth.models import User, Group
from musica.models import Cancion
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


class SongSerializer(serializers.HyperlinkedModelSerializer):
    # Obtenemos los datos del audio así: https://stackoverflow.com/a/27851778
    title = serializers.CharField(read_only=True, source="audio.titulo")
    file = serializers.FileField(read_only=True, source="audio.archivo")

    class Meta:
        model = Cancion
        fields = ['title', 'file']
