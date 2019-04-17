from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from .models import *

import json
import string

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
def testDirectSql(request):
    response = JsonResponse({'status': 'Server ready'})
    return response

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
        if comment == '':
            classification = 'There is nothing to classify here.'
        else:
            analysis = sibyl.sentiment_single(comment)      # pass the comment to the single classifier
            if analysis[0] == 'pos':
                classification = 'The phrase showed a positive polarity.'
            else:
                classification = 'The phrase showed a negative polarity.'

        # Format the classification (pos/neg)
        # for result in analysis:
        #     if result[0] == 'pos':
        #         classification = 'The phrase showed a positive polarity.'
        #     else:
        #         classification = 'The phrase showed a negative polarity.'

        # create a JSON response object using the analysis results
        # and return it back to the page
        response = JsonResponse({'result': classification})
        return response

# THE MODEL BYPASSING DIRECT SQL CREATE TABLE GOODNESS
@csrf_exempt
def createTable(request):
    # Retrieve all the data submitted from the frontend
    tableName = request.POST.get('tableName')
    fields = json.loads(request.POST.get('fields'))
    sql = "CREATE TABLE '%s' ('rowId' int NOT NULL, PRIMARY KEY('rowId'));" % tableName
    ## CODE BLOCK FOR CURSOR EXECUTION
    ## CLEANED FOR TESTING!
    ## TAKE NOTE THAT OBJECT NAMES HERE FOLLOW THE STANDARD NAMES GIVEN
    ## BY THE FORM BUILDER TO ITS CHILD ELEMENTS. SO LONG AS IT IS NOT REMOVED,
    ## THIS BLOCK WILL WORK ALL THE TIME.
    try:
        # Create the table first
        print('Creating table %s...' % tableName)
        print('Table created.\n\n')

        # Then alter it next
        try:
            print('Altering table...')
            for obj in fields:
                sql_begin = "ALTER TABLE '%s' ADD" % tableName

                if obj[0:5] == 'text-':
                    print('Object detected: %s' % obj[0:4])
                    object = "'%s' varchar(300);" % obj[5:]
                elif obj[0:7] == 'select-':
                    print('Object detected: %s' % obj[0:6])
                    object = "'%s' varchar(25);" % obj[7:]
                elif obj[0:9] == 'textarea-':
                    print('Object detected: %s' % obj[0:8])
                    object = "'%s' varchar(300);" % obj[9:]
                elif obj[0:12] == 'radio-group-':
                    print('Object detected: %s' % obj[0:11])
                    object = "'%s' varchar(25);" % obj[12:]
                else:
                    object =''

                if object != '':
                    sql_final = ' '.join([sql_begin, object])
                    print('Creating column for %s...' % obj)
                    print('Column created.\n\n')

                status = 'Process executed without errors.'

        except Exception as ex:
            status = ex

    except Exception as ex:
        status = ex

    # RETURN A JSON RESPONSE
    response = JsonResponse({'status': status, 'table-name': tableName, 'fields':fields}, safe=False)
    return response
