from models import Debate, Entry, Comment
from django.shortcuts import render_to_response
from django.db.models import Sum

def index(req):
  # list all debates by pubdate
  debates = Debate.objects.all().order_by('-pub_date')
  return render_to_response('index.html', {'debates': debates})

def getPoints(debate, user):
  return Comment.objects.filter(parentEntry__debate = debate, parentEntry__author = user).aggregate(Sum('parentPoints'))['parentPoints__sum']


def debate(req, id):
  debate = Debate.objects.get(id = id)
  c = { "debate": debate,
      "instigatorpoints": getPoints(debate, debate.instigator),
      "challengerpoints": getPoints(debate, debate.challenger),
      "entries": Entry.objects.filter(debate = debate)
      }
  return render_to_response('debate.html', c)
