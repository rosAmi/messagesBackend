from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     messages = serializers.HyperlinkedRelatedField(many=True, view_name='message-detail', read_only=True)
class UserSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'messages']


# class MessageSerializer(serializers.HyperlinkedModelSerializer):
#     sender = serializers.ReadOnlyField(source='sender.username')
class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
        # fields = ['id', 'subject', 'message', 'isRead', 'sender']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.message = validated_data.get('message', instance.message)
        instance.sender = validated_data.get('sender', instance.sender)
        instance.save()
        return instance
