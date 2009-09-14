from models import Debate
from django.shortcuts import render_to_response

def index(req):
  # list all debates by pubdate
  debates = Debate.objects.all().order_by('-pub_date')
  return render_to_response('index.html', {'debates': debates})

