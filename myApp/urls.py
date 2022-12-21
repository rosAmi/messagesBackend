from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename="message")
router.register(r'users', UserViewSet, basename="user")

urlpatterns = router.urls
# urlpatterns = [
#     path('', include(router.urls)),
# ]
