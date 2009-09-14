from models import Debate
from django.shortcuts import render_to_response

def index(req):
  # list all debates by pubdate
  debates = Debate.objects.all().order_by('-pub_date')
  return render_to_response('index.html', {'debates': debates})

def debate(req, id):
  debate = Debate.objects.get(id = id)
  c = { "debate": debate,
      "instigatorpoints": getInstigatorPoints(debate),
      "challengerpoints": getChallengerPoints(debate),
      }
  return render_to_response('debate.html', c)
