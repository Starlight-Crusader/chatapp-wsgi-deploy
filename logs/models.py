from django.db import models


class Log(models.Model):
    code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    resolved = models.BooleanField(default=False)
    origin_ip = models.CharField(null=True)
