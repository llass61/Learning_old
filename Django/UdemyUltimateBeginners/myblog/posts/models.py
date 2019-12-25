# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    pubDate = models.DateTimeField()
    image = models.ImageField(upload_to='media/')
    body = models.TextField()

    def __str__(self):
        return self.title
    

    def pubDateFmt(self):
        return self.pubDate.strftime('%b %d %Y')


    def summary(self):
        return self.body[:200]
