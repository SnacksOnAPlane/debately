from django.db import models
from django.contrib.auth.models import User

POINT_CHOICES = (
    (-1, -1),
    (0, 0),
    (1, 1),
    )

class Debate(models.Model):
  title = models.CharField(max_length = 200)
  summary = models.TextField() # not for the first entry!  just a summary, please
  pub_date = models.DateTimeField(auto_now_add = True)
  instigator = models.ForeignKey(User)

class Entry(models.Model):
  debate = models.ForeignKey(Debate)
  text = models.TextField()
  author = models.ForeignKey(User)
  pub_date = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
  author = models.ForeignKey(User)
  text = models.TextField()
  parentEntry = models.ForeignKey(Entry)
  parentComment = models.ForeignKey('self')
  pub_date = models.DateTimeField(auto_now_add = True)
  parentPoints = models.SmallIntegerField(choices = POINT_CHOICES)
