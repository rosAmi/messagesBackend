from django.db import models
from django.conf import settings


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    isRead = models.BooleanField(default=False, editable=False)
    sender = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.subject

