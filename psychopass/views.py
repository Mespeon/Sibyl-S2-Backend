from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

#Cross-app Model Referencing
from registry.models import UserAccount

#Cross-app Script Referencing
from registry import helloWorld
from . import lexAnalysis as lex
from . import sibyl

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
    if request.method == 'GET':
        return HttpResponse('A curious soul. Move along, there is nothing to see here.')
    else:
        # SAVE THIS PORTION AS REFERENCE FOR
        # PASSING A STRING LIST TO THE CLASSIFIER.
        # textSet = [
        # 'Amazing! The plot is good, the speakers did great. Overall, a really enjoyable seminar.',
        # 'That was really good. I enjoyed it.',
        # 'It could do better..',
        # 'Not good',
        # 'The seminar was awesome! The topic was great, activities were wonderful, and there were pythons...so yea!',
        # ]

        comment = request.POST.get('comment')           # get the comment (this is passed using an AJAX request)
        analysis = sibyl.sentiment_single(comment)      # pass the comment to the single classifier

        # Format the classification (pos/neg)
        # for result in analysis:
        #     if result[0] == 'pos':
        #         classification = 'The phrase showed a positive polarity.'
        #     else:
        #         classification = 'The phrase showed a negative polarity.'

        # create a JSON response object using the analysis results
        # and return it back to the page
        if analysis[0] == 'pos':
            classification = 'The phrase showed a positive polarity.'
        else:
            classification = 'The phrase showed a negative polarity.'

        response = JsonResponse({'result': classification})
        return response
