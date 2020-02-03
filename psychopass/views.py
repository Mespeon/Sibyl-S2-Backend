from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import django.middleware.csrf as csrf

from .models import *

import json
import string
import sqlite3 as db
from datetime import datetime

#Cross-app Model Referencing
from registry.models import UserAccount

#Cross-app Script Referencing
from registry import helloWorld
from . import lexAnalysis as lex
# from . import sibyl
# from . import randomizer
from . import stargazer as strg

def index(request):
    return HttpResponse('You have reached Sibyl.')

# Remove this after testing
# Cascade to models as well, if needed.
def testView(request):
    return render(request, 'psychopass/options.html', {})

def thanks(request):
    return render(request, 'psychopass/thankYou.html', {})

@csrf_exempt
def stargazer(request):
	if request.method == 'GET':
		lovelive = strg.preparePayload()
		response = JsonResponse({'data': lovelive}, safe=False)
		return response

@csrf_exempt
def stars(request):
    if request.method == 'GET':
        responseData = []
        responseMessage = ''

        #Get all parameters passed to the API.
        paramsReceived = request.GET.dict()
        print(paramsReceived)

        # Check if there are parameters passed,
        # then return a corresponding value.
        if len(paramsReceived) > 0:
            responseData.append(paramsReceived)
            responseMessage = 'There are %d parameters received.' % len(paramsReceived)
        else:
            responseMessage = 'There are %d parameters received.' % len(paramsReceived)

        response = JsonResponse({
        'paramsReceived': responseData,
        'message': responseMessage
        }, safe=False)

        return response
