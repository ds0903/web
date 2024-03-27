from django.db import models

class Issue(models.Model): #noqa
    juni_id = models.IntegerField(max_length=5)
    seni_id = models.IntegerField(max_length=5)
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=100)
