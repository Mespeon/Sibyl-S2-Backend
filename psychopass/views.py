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
from . import sibyl
from . import randomizer
from . import stargazer as strg
# from . import senpai

def index(request):
    return HttpResponse('You have reached Sibyl.')

# Remove this after testing
# Cascade to models as well, if needed.
def testView(request):
    return render(request, 'psychopass/options.html', {})

def thanks(request):
    return render(request, 'psychopass/thankYou.html', {})

# Front-end communication preparations
@csrf_exempt
def prepareData(request):
    if request.method == 'GET':
        # Simply return something in JSON. This is just a status request, anyway.
        response = JsonResponse({'message': '[Sibyl Endpoint] You have reached Sibyl.'})
        return response
    else:
        form = request.POST.copy()
        formId = request.POST.get('text--formId')
        status = 'A status message should be returned.'

        # Perform a statistics request sequence
        with connection.cursor() as cursor:
            # Perform a table lock
            try:
                sql = "SELECT * FROM `%s`" % form.get('text--formId')
                cursor.execute(sql)
                row = cursor.fetchall()
                row_count = len(row)
                print(row)

                # Perform a column count
                try:
                    column_check = "PRAGMA table_info(`%s`)" % form.get('text--formId')
                    column_lock = cursor.execute(column_check)
                    columns = len([description[0] for description in column_lock])

                    name_lock = cursor.execute(column_check)
                    names = [description[1] for description in name_lock]

                    print(names)

                except Exception as ex:
                    status = ex

            except Exception as ex:
                status = ex

        # Prepare values to be returned
        status = 'Data successfully retrieved.'
        return_row = row
        return_row_count = row_count
        return_col_count = columns
        return_col_names = names

        # Return a JSON response
        response = JsonResponse({'status': status,
        'received': formId,
        'rows': return_row,
        'cols': return_col_names,
        'colsCount': return_col_count,
        'rowsCount': return_row_count}, safe=False)
        return response

#Statistical data pull
@csrf_exempt
def prepareStatistics(request):
    if request.method == 'GET':
        return HttpResponse('Okaaay, so you reached me. But I won\'t talk unless you give me what I need.')
    else:
         # This should come from the extension, sent by the selector on value change on specific values.
        form = request.POST.get('formId')
        column = request.POST.get('column')
        status = 'This should be overwritten after the process.'
        distinctValueSet = []
        distinctValueCount = []
        distinctPercentage = []

        # Perform column statistics on the selected column
        with connection.cursor() as cursor:
            try:
                # Perform a query for DISTINCT and COUNT(entry) values GROUPED BY column
                sql = 'SELECT DISTINCT `%s` AS "distinctValues", COUNT(`%s`) AS "entryCount" FROM `%s` GROUP BY `%s`' % (column, column, form, column)
                cursor.execute(sql)
                row = cursor.fetchall()
                print(row)

                # Append distinct values and count to respective array
                for i in range(0, len(row), 1):
                    distinctValueSet.append(row[i][0])

                for i in range(0, len(row), 1):
                    distinctValueCount.append(row[i][1])

                # Execute a separate query to get the actual row count of the table
                sql_table_length = 'SELECT rowId FROM `%s`' % form
                cursor.execute(sql_table_length)
                entry_count = cursor.fetchall()
                print(len(entry_count))

                # Perform percentage calculations on distinct counts
                row_count = len(entry_count)
                for i in range(0, len(distinctValueCount), 1):
                    percentage = (distinctValueCount[i] / row_count) * 100
                    percentage_formatted = '{:.2f}'.format(percentage)
                    distinctPercentage.append(percentage_formatted)

                # Return an OK status if this try block executes successfully.
                status = '200 OK'
            except Exception as ex:
                print(ex)
                status = 'Process failed.'

        # Prepare values to be returned
        distinct = distinctValueSet
        distCount = distinctValueCount
        distDistribution = distinctPercentage

        # Prepare JSON response
        response = JsonResponse({'status': status,
        'distinctValues': distinct,
        'distinctCount': distCount,
        'distinctDistribution': distDistribution}, safe=False)
        return response

# Lexicon Match sentiment analysis algorithm
# This is used in the Developers Option's LM Tester.
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

# Naive Bayes classifier sentiment analysis algorithm
# This is used in the Developers Option's NB Classifier Tester.
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

        # The actual sentiment analysis request
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

# Aggregated Naive Bayes Classification
# Used for the actual classification on entry sets.
@csrf_exempt
def aggregatedClassify(request):
    if request.method == 'GET':
        return HttpResponse('This is not the droid you are looking for. Move along.')
    else:
        # Determine which column (or entry set as we'll call here) needs to be classified.
        formId = request.POST.get('formId')
        entrySet = request.POST.get('request');

        # Default values
        status = 0
        textSet = []
        classification = ''
        entryClassification = []
        positives = 0
        negatives = 0
        p_average = 0
        n_average = 0
        positiveLex = []
        negativeLex = []

        # Try to lock on the table
        with connection.cursor() as cursor:
            try:
                sql = "SELECT %s FROM `%s`" % (entrySet, formId)
                cursor.execute(sql)
                rows = cursor.fetchall()

                # Append the fetched rows to an array
                for v in rows:
                    textSet.append(v)

                # Then pass the array to the sentiment analysis script.
                if len(textSet) == 0:
                    classification = 'There is nothing to classify here.'
                else:
                    # Iterate through each item in the entry set
                    # This loop is for the NB classifier.
                    print('Requesting classification from Classifier-chan...')
                    ctr = 0
                    for i in textSet:
                        analysis = sibyl.sentiment_single(str(i))      # pass the comment to the single classifier
                        if analysis[0] == 'pos':
                            positives += 1
                            entryClassification.append(analysis[0])
                        else:
                            negatives += 1
                            entryClassification.append(analysis[0])

                        ctr += 1

                    print(entryClassification)
                    # This loop is for the lexicon matcher for polarized words
                    print('Requesting lexicon match from Lexicon-kun...')
                    for m in textSet:
                        analysisLex = lex.LexiconAnalysis.beginLexAnalysis(str(m))

                        # Append positive and negative lex matches to array
                        for lexus in analysisLex[4]:
                            positiveLex.append(lexus)

                        for lexus in analysisLex[5]:
                            negativeLex.append(lexus)

                    # Classification
                    if positives > negatives:
                        classification = 'The entry set showed positive sentiment.'
                    elif negatives > positives:
                        classification = 'The entry set showed negative sentiment.'
                    else:
                        classification = 'The entry set is neutral.'

                    # Averaging
                    p_average = (positives / len(textSet)) * 100
                    n_average = (negatives / len(textSet)) * 100

                    p_adjusted = '{:.2f}'.format(p_average)
                    n_adjusted = '{:.2f}'.format(n_average)

                    # Return a 200 OK status
                    status = 200

            except Exception as ex:
                print(ex)
                status = 'Process failed.'

        # Return a JSON response
        response = JsonResponse({'status': status,
        'formId': formId,
        'entrySet': entrySet,
        'entryCount': len(textSet),
        'classification': classification,
        'entryClassification': entryClassification,
        'positives': positives,
        'negatives': negatives,
        'positiveAverage': p_adjusted,
        'negativeAverage': n_adjusted,
        'positiveLexes': positiveLex,
        'negativeLexes': negativeLex}, safe=False)
        return response

# THE MODEL BYPASSING DIRECT SQL CREATE TABLE GOODNESS
@csrf_exempt
def createTable(request):
    if request.method == 'GET':
        return HttpResponse('This is not the droid you are looking for. Move along.')
    else:
        # Retrieve all the data submitted from the frontend
        tableName = request.POST.get('tableName')
        fields = json.loads(request.POST.get('fields'))

        #sql = "CREATE TABLE '%s' ('rowId' int NOT NULL AUTO_INCREMENT, PRIMARY KEY('rowId'));" % tableName
        sql_lite = "CREATE TABLE '%s' ('rowId' INTEGER PRIMARY KEY);" % tableName
        ## CODE BLOCK FOR CURSOR EXECUTION
        ## CLEANED FOR TESTING!
        ## TAKE NOTE THAT OBJECT NAMES HERE FOLLOW THE STANDARD NAMES GIVEN
        ## BY THE FORM BUILDER TO ITS CHILD ELEMENTS. SO LONG AS IT IS NOT REMOVED,
        ## THIS BLOCK WILL WORK ALL THE TIME.
        with connection.cursor() as cursor:
            try:
                # Create the table first
                print('Creating table %s...' % tableName)
                cursor.execute(sql_lite);
                print('Table created.\n\n')

                # Then alter it next
                try:
                    print('Altering table...')
                    for obj in fields:
                        sql_begin = "ALTER TABLE '%s' ADD" % tableName

                        if obj[0:5] == 'text-':
                            # FOR TEXT FIELDS
                            print('Object detected: %s' % obj[0:4])
                            object = "'%s' varchar(300);" % obj[5:]
                        elif obj[0:7] == 'select-':
                            # FOR SELECT GROUPS
                            print('Object detected: %s' % obj[0:6])
                            #object = "'%s' varchar(25);" % obj[7:]
                            object = "'%s' varchar(25);" % obj
                        elif obj[0:9] == 'textarea-':
                            # FOR TEXT AREAS
                            print('Object detected: %s' % obj[0:8])
                            object = "'%s' varchar(300);" % obj[9:]
                        elif obj[0:12] == 'radio-group-':
                            # FOR RADIO GROUPS
                            print('Object detected: %s' % obj[0:11])
                            #object = "'%s' varchar(25);" % obj[12:]
                            object = "'%s' varchar(25);" % obj
                        elif obj[0:15] == 'checkbox-group-':
                            # FOR CHECKBOX GROUPS
                            print('Object detected: %s' % obj[0:14])
                            #object = "'%s' varchar(25);" % obj[15:]
                            object = "'%s' varchar(25);" % obj
                        elif obj[0:5] == 'date-':
                            # FOR DATE FIELDS
                            print('Object detected: %s' % obj[0:4])
                            object = "'%s' varchar(25);" % obj[5:]
                        elif obj[0:7] == 'hidden-':
                            # FOR HIDDEN FIELDS
                            print('Object detected: %s' % obj[0:6])
                            object = "'%s' varchar(50);" % obj[7:]
                        elif obj[0:7] == 'number-':
                            # FOR NUMBER FIELDS
                            print('Object detected: %s' % obj[0:6])
                            object = "'%s' varchar(15);" % obj[7:]
                        else:
                            object =''

                        if object != '':
                            sql_final = ' '.join([sql_begin, object])
                            print('Creating column for %s...' % obj)
                            cursor.execute(sql_final);
                            print('Column created.\n\n')

                        status = '[Sibyl Endpoint] Process executed without errors.'

                except Exception as ex:
                    status = ex

            except Exception as ex:
                status = ex

        print(str(status))
        # RETURN A JSON RESPONSE
        response = JsonResponse({'status': str(status), 'table-name': tableName, 'fields':fields}, safe=False)
        return response

# Dynamic table writer
@csrf_exempt
def writeToTable(request):
    if request.method == 'POST':
        # form = request.POST
        tableName = request.POST.get('tableName')
        fields = json.loads(request.POST.get('formData'))
        #form_body = json.loads(request.body)

        # Form data print FOR THE LULLLZZZZZ
        print(tableName)
        for f in range(1, len(fields), 1):
            print(fields[f])

        # Form data debug
        # print('Items')
        # for i in form.items():
        #     print(i)
        #
        # print('\nValues only')
        # for v in form.values():
        #     print(v)

        status = 0

        # The actual WRITE process
        with connection.cursor() as cursor:
            # Table lock
            table_lock = "SELECT * FROM '%s'" % tableName
            try:
                locked_table = cursor.execute(table_lock)
                # Check if the table exists, if TRUE, try accessing the columns first,
                # then appending their names to an INITIAL INSERT INTO SQL.
                if locked_table:
                    status = 'Table found!'
                    print('\n\n',status)
                    try:
                        column_check = "PRAGMA table_info('%s')" % tableName
                        column_lock = cursor.execute(column_check)
                        # This will only be executed if the table exists AND there are columns in it.
                        if column_lock:
                            initial_insert_sql = "INSERT INTO `%s` (" % tableName
                            names = [description[1] for description in column_lock]
                            print('Number of columns in table: ', len(names))

                            # Loop through the column names (excluding the rowId column)
                            # and join it with the initial INSERT INTO query.
                            for col in range(1, len(names), 1):
                                colName = "`%s`" % names[col]
                                if col < len(names)-1:
                                    initial_insert_sql = ''.join([initial_insert_sql, colName, ','])
                                elif col == len(names)-1:
                                    initial_insert_sql = ''.join([initial_insert_sql, colName, ')'])

                            print('\n\nProgramatically generated INSERT INTO query:')
                            print(initial_insert_sql)

                            # Loop through the form values (excluding the hidden form ID)
                            # and join it with the initial VALUES query
                            initial_values_sql = "VALUES ("
                            field_values = []   # array for field values

                            # Get the field values then append it to the array above.
                            for v in fields:
                                field_values.append(v)

                            # Loop through the values (excluding the hidden form ID)
                            for val in range(1, len(field_values), 1):
                                value = "'%s'" % field_values[val]    # Format each value to be quote enclosed first.

                                # Then join it to the VALUES query
                                if val < len(field_values) - 1:
                                    initial_values_sql = ''.join([initial_values_sql, value, ','])
                                elif val == len(field_values) - 1:
                                    initial_values_sql = ''.join([initial_values_sql, value, ')'])

                            print('\n\nProgramatically generated VALUES query:')
                            print(initial_values_sql)

                            # Construct the final SQL query
                            sql_final = ' '.join([initial_insert_sql, initial_values_sql])
                            print('\n\nProgramatically generated INSERT INTO VALUES query:')
                            print(sql_final)

                            # Try and execute the FINAL query. THIS WILL INSERT THE VALUES INTO
                            # THE TABLE IDENTIFIED BY THE HIDDEN INPUT VALUE.
                            try:
                                print('Executing final query...')
                                cursor.execute(sql_final)
                                print('\n\nValues successfully saved.')
                                status = 200
                            except Exception as ex:
                                print(ex)
                                status = ex

                    except Exception as ex:
                        print(ex)
                        status = ex

            except Exception as ex:
                print(ex)
                status = ex

        #print(status)
        # Return a JSON response
        response = JsonResponse({'response': 'You have reached the writer.', 'status': status}, safe=False)
        return response
    else:
        return HttpResponse('You have reached a place not meant for humans. Consider turning around.')

## IONIC APP TEST VIEWS
@csrf_exempt
def testComms(request):
	if request.method == 'GET':
		randomizedQuote = randomizer.getRandomQuote()
		response = JsonResponse({'message': randomizedQuote, 'status': '0'}, safe=False)
		return response
	else:
		data = request.POST.get('message')
		response = JsonResponse({'reply': 'Hello there! It seems you sent me something.', 'data': data, 'status': '0'}, safe=False)
		return response

@csrf_exempt
def stargazer(request):
	if request.method == 'GET':
		lovelive = strg.preparePayload()
		response = JsonResponse({'data': lovelive}, safe=False)
		return response

def forVivien(request):
    return render(request, 'psychopass/senpai.html', {})

@csrf_exempt
def forSenpai(request):
    message = 'Overwrite this with something.'
    isCorrect = 0
    status = 4

    # Determine first if the request is a GET or POST
    if request.method == 'GET':
        return HttpResponse('GET?')
    else:
        # Try to get the data from the form first,
        # then return a JSON response.
        try:
            data = request.POST.get('answer')
            print(data)

            if data == 'VIVIEN':
                message = "Congratulations, it's the correct answer! Kindly take a screenshot of this page and show it to Adrine~"
                isCorrect = 1
            else:
                message = "Aww. Try again. :)"
                isCorrect = 0

            status = 0
        except Exception as ex:
            message = ex
            status = 1

    # Return the response
    response = JsonResponse({'status': status, 'isCorrect': isCorrect, 'message': message}, safe=False)
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

@csrf_exempt
def coeLike(request):
    if request.method == 'GET':
        # For GET requests, simply return the length of the table.
        error = 0
        status = 'Overwrite this with a new message.'
        data = ''
        with connection.cursor() as cursor:
            try:
                sql = "SELECT * FROM `likes`"
                cursor.execute(sql)
                rows = cursor.fetchall()

                # Append the fetched rows to an array
                rowCount = []  # Overwrite this with a new value to check for validity.
                for v in rows:
                    rowCount.append(v)

                data = {'length': len(rowCount)}
                status = 'OK'
            except Exception as ex:
                print('Error GETting likes: ', ex)
                status = 'Error GETting likes %s' % ex
                error = 1
                data = 'No data available.'

        response = JsonResponse({
        'error': error,
        'status': status,
        'data': data
        }, safe=False)

        return response

    else:
        # For POST requests
        likeFrom = request.POST.get('likeFrom')
        error = 0
        status = 'Overwrite this with a new message.'

        with connection.cursor() as cursor:
            # Table lock
            table_lock = "SELECT * FROM 'likes'"
            try:
                locked_table = cursor.execute(table_lock)
                if locked_table:
                    print('Table found! Writing data...')
                    try:
                        query = 'INSERT INTO `likes` (`from`) VALUES ("%s")' % likeFrom
                        print('Query: ', query)

                        cursor.execute(query)
                        status = 'OK'
                    except Exception as ex:
                        print('Error writing to table: ', ex)
                        status = 'Error writing to table: %s' % ex
                        error = 1
            except Exception as ex:
                print('Error POSTing like: ', ex)
                status = 'Error POSTing like: %s' % ex
                error = 1

        response = JsonResponse({
        'error': error,
        'status': status,
        }, safe=False)

        return response

@csrf_exempt
def coeReact(request):
    if request.method == 'GET':
        return HttpResponse('You want to react on the COE Toothbrush?')
    else:
        return HttpResponse('I see you wanna react to the COE Toothbrush.')

@csrf_exempt
def createApiTable(request):
    error = 0
    status = ''

    if request.method == 'GET':
        return HttpResponse('Hey, an unfamiliar face. What brings you here?')
    else:
        # This will only work if the request has a Content-Type of 'application/json'
        # and the form body is JSON.stringified. Otherwise, it may fail on other Content-Types.
        form = json.loads(request.body.decode())
        tableName = form['tblName']
        tableCols = form['tblCols']

        sql_createTable = "CREATE TABLE '%s' ('rowId' INTEGER PRIMARY KEY);" % tableName
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_createTable)

                try:
                    sql_alterTable = "ALTER TABLE '%s' ADD" % tableName
                    for obj in tableCols:
                        object = "'%s' varchar(50);" % obj

                        if object != '':
                            sql_adjusted = ' '.join([sql_alterTable, object])
                            cursor.execute(sql_adjusted)

                    error = 0
                    status = 'OK'
                except Exception as ex:
                    error = 1
                    status = ex

            except Exception as ex:
                error = 1
                status = ex

        return JsonResponse({
        'error': error,
        'status': status
        }, safe=False)

@csrf_exempt
def getToken(request):
    error = 0
    status = ''
    token = 'No token issued.'

    if request.method == 'POST':
        try:
            getAToken = csrf.get_token(request)
            timeNow = datetime.now()
            # After getting a csrf_token, write it into the device_tokens table.
            # This table will hold all the issued CSRF token by the middleware.
            # All tokens in the table will be validated by the auth view whenever
            # a request is trying to access a protected view.
            #
            # FOR SECURITY PURPOSES, WHENEVER THE LOGOUT VIEW IS CALLED, WE SHOULD
            # REMOVE THE CSRF_TOKEN FROM THE DEVICE_TOKENS TABLE. THIS IS TO PREVENT
            # TOKEN LEAKAGE AND POSSIBLE TOKEN REUSE.
            #
            # FOR NOW, THIS APPROACH IS TEMPORARY UNTIL JWT AND FCM IS INTEGRATED
            # IN THIS PROJECT.
            # initial_insert_sql = "INSERT INTO `%s` (" % tableName
            sql_writeToken = 'INSERT INTO `device_tokens` (`token`, `created_at`) VALUES ("%s", "%s")' % (getAToken, timeNow)
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_writeToken)
                    status = 'OK'
                    token = getAToken
                except Exception as ex:
                    error = 0
                    status = ex

        except Exception as ex:
            error = 1
            status = ex

        return JsonResponse({
        'error': error,
        'status': status,
        'token': token
        }, safe=False)
    else:
        return HttpResponse('You are not meant to be here.')

@csrf_exempt
def getAuth(request):
    # If error is still set at -1, it means this function failed to do its thing.
    error = -1
    status = 'Unauthorized'
    data = {}

    if request.method == 'POST':
        # Get the submitted token first.
        form = json.loads(request.body.decode())
        thisToken = form['token']

        # Authenticate the token first.
        with connection.cursor() as cursor:
            try:
                sql_validateToken = 'SELECT `token` from `device_tokens` WHERE `token` == "%s"' % thisToken
                cursor.execute(sql_validateToken)
                if sql_validateToken:
                    myToken = cursor.fetchall()
                    if len(myToken) > 0:
                        error = 0
                        status = 'Authorized'
                        data = {'token': myToken[0]}
                    else:
                        error = 1
                        status = 'Invalid token'
                else:
                    error = 1
                    status = 'Invalid token'
            except Exception as ex:
                error = 1
                status = 'Failed to authenticate token'
    else:
        return HttpResponse('You are not supposed to be here.')

    return JsonResponse({
    'error': error,
    'status': status,
    'data': data
    }, safe=False)

@csrf_exempt
def register(request):
    error = -1
    status = 'Undetermined'
    data = {}

    if request.method == 'POST':
        form = json.loads(request.body.decode())

        # Fork here first to check if the registration is from social or not.
        if form['isSocial']:
            pass
        else:
            pass

        return JsonResponse({
        'error': error,
        'status': status,
        'data': data
        }, safe=False)
    else:
        return HttpResponse('Curious, aren\'t you?')

@csrf_exempt
def login(request):
    error = -1
    status = 'Undetermined'
    data = {}

    if request.method == 'POST':
        form = json.loads(request.body.decode())

        if form['isSocial']:
            pass
        else:
            pass

        return JsonResponse({
        'error': error,
        'status': status,
        'data': data
        }, safe=False)
    else:
        return HttpResponse('Why are you still here? You are not allowed inside, anyway.')

    return JsonResponse({
    'error': error,
    'status': status,
    'data': data
    }, safe=False)

@csrf_exempt
def logout(request):
    error = -1
    status = 'Undetermined'
    data = {}

    if request.method == 'POST':
        form = json.loads(request.body.decode())
        myToken = form['token']

        # Match the token given by the logout request, then remove it from the table.
        with connection.cursor() as cursor:
            sql_getToken = 'SELECT `token` FROM `device_tokens` WHERE `token` == "%s"' % myToken
            try:
                cursor.execute(sql_getToken)
                token = cursor.fetchall()

                if len(token) > 0:
                    sql_removeToken = 'DELETE from `device_tokens` WHERE `token` == "%s"' % myToken
                    try:
                        cursor.execute(sql_removeToken)

                        error = 0
                        status = 'OK'
                    except Exception as ex:
                        error = 1
                        status = 'Failed to remove token'
                else:
                    error = 1
                    status = 'No valid token found'
            except Exception as ex:
                error = 1
                status = ex
    else:
        return HttpResponse('Aaaggghh for the nth time!')

    return JsonResponse({
    'error': error,
    'status': status,
    'data': data
    }, safe=False)

@csrf_exempt
def listing(request):
    error = -1
    status = 'Undetermined'
    data = {}

    if request.method == 'GET':
        responseMessage = ''

        #Get all parameters passed to the API.
        paramsReceived = request.GET.dict()
        print(paramsReceived)

        # 'paramsReceived': responseData,
        # 'message': responseMessage
        # Check if there are parameters passed,
        # then return a corresponding value.
        if len(paramsReceived) > 0:
            error = 0
            data['params'] = paramsReceived
            status = 'There are %d parameters received.' % len(paramsReceived)
        else:
            error = 0
            status = 'There are %d parameters received.' % len(paramsReceived)

        return JsonResponse({
        'error': error,
        'status': status,
        'data': data
        }, safe=False)

    else:
        return HttpResponse('You posted this request, didn\'t you?')

@csrf_exempt
def authlisting(request):
    error = -1
    status = 'Undetermined'
    data = {}

    if request.method == 'POST':
        error = 0
        status = 'OK'

        return JsonResponse({
        'error': error,
        'status': status,
        'data': data
        }, safe=False)
    else:
        return HttpResponse('OH, YOU\'RE APPROACHING ME?!')

@csrf_exempt
def ultraEquipment(request):
    error = -1
    status = ''
    data = []

    if request.method == 'POST':
        # This will only work if the request has a Content-Type of 'application/json'
        # and the form body is JSON.stringified. Otherwise, it may fail on other Content-Types.
        form = json.loads(request.body.decode())
        col = form['part']

        with connection.cursor() as cursor:
            query = "SELECT * FROM ultra_equipment WHERE `class` == '%s'" % col
            try:
                cursor.execute(query)
                equipmentSpecific = cursor.fetchall()

                if (len(equipmentSpecific) > 0):
                    for item in equipmentSpecific:
                        itemObj = {
                        'id': item[0],
                        'class': item[1],
                        'name': item[2],
                        'description': item[3]
                        }
                        data.append(itemObj)

                    error = 0
                    status = 'OK'
                else:
                    status = 'OK - no data found'
                    error = 0
            except Exception as ex:
                status = ex
                error = 1
    else:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM ultra_equipment'
            try:
                cursor.execute(query)
                equipment = cursor.fetchall()

                if (len(equipment) > 0):
                    for item in equipment:
                        itemObj = {
                        'id': item[0],
                        'class': item[1],
                        'name': item[2],
                        'description': item[3]
                        }
                        data.append(itemObj)

                    error = 0
                    status = 'OK'
                else:
                    status = 'OK - no data found'
                    error = 0
            except Exception as ex:
                error = 1
                status = ex

    return JsonResponse({
    'error': error,
    'status': status,
    'data': data
    }, safe=False)

@csrf_exempt
def ultraAddEquipment(request):
    error = -1
    status = ''
    data = []

    if request.method == 'POST':
        form = json.loads(request.body.decode())
        table = form['table']
        name = form['name']
        className = form['class']
        desc = form['description']

        with connection.cursor() as cursor:
            lastId = 0
            tableName = 'ultra_%s' % table
            queryGetId = 'SELECT * FROM `%s`' % tableName
            queryPost = 'INSERT INTO `%s` (`equipId`, `class`, `name`, `description`) VALUES ("%s", "%s", "%s", "%s")' % (tableName, lastId, className, name, desc)
            try:
                cursor.execute(queryGetId)
                id = cursor.fetchall();
                lastId = len(id) + 1
                try:
                    cursor.execute(queryPost)
                    error = 0
                    status = 'OK'
                    data = {
                    'table': tableName,
                    'name': name,
                    'class': className,
                    'description': desc
                    }
                except Exception as ex:
                    error = 1
                    status = ex
                #
                # error = 0
                # status = 'OK'
                # data = {
                # 'table': tableName,
                # 'name': name,
                # 'class': className,
                # 'description': desc
                # }
            except Exception as ex:
                error = 1
                status = ex
    else:
        error = 1
        status = 'You are not supposed to be here.'

    return JsonResponse({
    'error': error,
    'status': status,
    'data': data
    })
