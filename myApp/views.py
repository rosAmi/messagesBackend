from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Message
from .serializer import MessageSerializer
from .serializer import UserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class HomePageView(TemplateView):
    template_name = "home.html"


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

