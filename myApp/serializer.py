from rest_framework.serializers import ModelSerializer

from .models import Message


class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
