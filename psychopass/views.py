from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

#Cross-app Model Referencing
from registry.models import UserAccount

#Cross-app Script Referencing
from registry import helloWorld
from . import lexAnalysis as lex

def index(request):
    return HttpResponse('You have reached Sibyl.')

# Remove this after testing
# Cascade to models as well, if needed.
def testView(request):
    return render(request, 'psychopass/options.html', {})

@csrf_exempt
def analyzeLexiconMatching(request):
    if request.method == 'GET':
        getMessage = lex.LexiconAnalysis.returnMessage('Have you tried submitting something to me? \'Coz I recieved nothing.')
        return HttpResponse(getMessage)
    else:
        comment = request.POST.get('comment')
        analysis = lex.LexiconAnalysis.beginLexAnalysis(comment)
        response = JsonResponse({'result' : analysis[3]})
        return response

@csrf_exempt
def analyzeClassifier(request):
    return HttpResponse('Classifier Analysis')
