from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Event(models.Model):
    date = models.DateField(blank=True, null=True)
    house = models.CharField(max_length=999)
    location = models.CharField(max_length=999)
    title = models.CharField(max_length = 999)
    description = models.CharField(max_length=999)
    def __unicode__(self):
        return unicode(self.title)

class Consultation(models.Model):
    gov_id = models.CharField(max_length=20)
    date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length = 500)
    summary = models.CharField(max_length = 500)
    url = models.CharField(max_length = 500)
    def __unicode__(self):
        return self.title
