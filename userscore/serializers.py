from rest_framework import serializers
from .models import User, Levels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User    
        fields = 'id','name','score'


class LevelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Levels
        fields = ['id', 'name', 'level_score', 'level_id']

    def get_name(self, levels):
        try:
            return levels.user.name
        except:
            return ""
