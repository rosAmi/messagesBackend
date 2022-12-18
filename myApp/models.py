from django.db import models


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    isRead = models.BooleanField(default=False)
    sender = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)
    # receiver = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.subject
