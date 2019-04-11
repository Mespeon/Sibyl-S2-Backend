from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

#Cross-app Model Referencing
from registry.models import UserAccount

#Cross-app Script Referencing
from registry import helloWorld

def index(request):
    return HttpResponse('You have reached Sibyl.')

def testView(request):
    return render(request, 'psychopass/options.html', {})

@csrf_exempt
def analyzeThis(request):
    return HttpResponse('Hello Analysis')
