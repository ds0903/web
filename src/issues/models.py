from django.db import models


class Issue(models.Model):
    juni_id = models.IntegerField()
    seni_id = models.IntegerField()
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=100)
