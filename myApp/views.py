from rest_framework.viewsets import ModelViewSet

from .models import Message
from .serializer import MessagesSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessagesSerializer
