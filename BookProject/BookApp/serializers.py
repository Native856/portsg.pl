from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="BookApp:user-detail")
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'BookApp:user-detail'},

            # Added this line:
            'groups': {'view_name': 'BookApp:group-detail'},
        }
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'BookApp:user-detail'},

            # Added this line:
            'groups': {'view_name': 'BookApp:group-detail'},
        }
        model = Group
        fields = ['url', 'name']