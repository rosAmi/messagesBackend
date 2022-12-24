from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, UserViewSet, MyMessages, MyInbox, MyInboxUnread, MyListView

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename="message")  # Admin only
router.register(r'mymessages', MyMessages, basename="mymessage")
router.register(r'myinbox', MyInbox, basename="myinbox")
router.register(r'myinboxunread', MyInboxUnread, basename="myinboxunread")
router.register(r'mylistview', MyListView, basename="mylistview")
router.register(r'users', UserViewSet, basename="user")

urlpatterns = router.urls
