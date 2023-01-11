from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import loader
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Message
from .serializer import MessageSerializer, MessageSerializerAll
from .serializer import UserSerializer
from rest_framework import permissions, status
from .permissions import IsOwnerOrReadOnly


class HomePageView(TemplateView):
    template_name = "home.html"


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(ModelViewSet):  # All messages in app **for Admin only**
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MyMessages(ViewSet):  # Get All my sent/receive messages
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request):
        # user = self.request.user
        if request.user.id is None:
            return Response({"detail": "Authentication credentials were not provided."})
        ids = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).values_list('id', flat=True)
        queryset = Message.objects.filter(pk__in=ids)
        serializer = MessageSerializerAll(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.id is None:
            return Response({"detail": "Authentication credentials were not provided."})
        ids = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).values_list('pk', flat=True)
        queryset = Message.objects.filter(pk__in=ids)
        message = get_object_or_404(queryset, pk=pk)  #
        serializer = MessageSerializerAll(message)
        if request.user.id == message.receiver.id:  # mark message as is_read=true
            message_obj = Message.objects.get(pk=pk)
            message_obj.isRead = True
            message_obj.save()
        return Response(serializer.data)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user)
            return Response({'status': 'issue created'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).values()
        try:
            message_obj = get_object_or_404(queryset, pk=pk)  # required for action authorization
            instance = Message.objects.get(pk=pk)
            instance.delete()
        except Http404:
            return Response(data='delete failed, un-authorized action')
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyInbox(ModelViewSet):  # all inbox messages read/unread
    serializer_class = MessageSerializerAll
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'head']  # , 'post', 'delete'

    def get_queryset(self):
        user = self.request.user
        ids = Message.objects.filter(receiver=user).values_list('id', flat=True)
        queryset = Message.objects.filter(pk__in=ids)
        return queryset


class MyInboxUnread(ModelViewSet):  # all unread messages
    serializer_class = MessageSerializerAll
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'head']  # , 'post', 'delete'

    def get_queryset(self):
        user = self.request.user
        ids = Message.objects.filter(receiver=user, isRead=False).values_list('id', flat=True)
        queryset = Message.objects.filter(pk__in=ids)
        return queryset


class MyListView(ViewSet):
    serializer_class = MessageSerializerAll
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        user = self.request.user
        queryset = Message.objects.filter(Q(sender=user) | Q(receiver=user)).values()
        template = loader.get_template('template.html')
        context = {
            'mymessages': queryset,
        }
        return HttpResponse(template.render(context, request))
