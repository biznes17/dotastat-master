from django.shortcuts import render
from django import template
from .models import *
from .forms import *

import requests

register = template.Library()


def mainPage(request):

	return render(request, 'dotastat/main.html')

def showMatchInfo(request):

	match_id = request.POST.get('get_match','')
	if match_id.isdigit():
		current_match = Match()
		current_match.initialize_match(match_id)
	else:
		current_match = Match()




	context={
	'match_id':match_id,
	'match': current_match,
	'players': current_match.players,
	}

	return render(request, 'dotastat/index.html', context=context)
