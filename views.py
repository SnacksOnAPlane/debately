from models import Debate, Entry, Comment
from django.shortcuts import render_to_response
from django.db.models import Sum

def index(req):
  # list all debates by pubdate
  debates = Debate.objects.all().order_by('-pub_date')
  return render_to_response('index.html', {'debates': debates})

def getDebatePoints(debate, user):
  return Comment.objects.filter(parentEntry__debate = debate, parentEntry__author = user, parentComment = None).aggregate(Sum('parentPoints'))['parentPoints__sum']

def getCommentPoints(debate, user):
  raise Exception("not implemented yet")

def debate(req, id):
  debate = Debate.objects.get(id = id)
  c = { "debate": debate,
      "instigatorpoints": getDebatePoints(debate, debate.instigator),
      "challengerpoints": getDebatePoints(debate, debate.challenger),
      "entries": Entry.objects.filter(debate = debate)
      }
  return render_to_response('debate.html', c)
