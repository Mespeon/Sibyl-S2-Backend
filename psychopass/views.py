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
        'received': form,
        'rows': return_row,
        'cols': return_col_names,
        'colsCount': return_col_count,
        'rowsCount': return_row_count}, safe=False)
        return response

# Lexicon Match sentiment analysis algorithm
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
                        object = "'%s' varchar(25);" % obj[7:]
                    elif obj[0:9] == 'textarea-':
                        # FOR TEXT AREAS
                        print('Object detected: %s' % obj[0:8])
                        object = "'%s' varchar(300);" % obj[9:]
                    elif obj[0:12] == 'radio-group-':
                        # FOR RADIO GROUPS
                        print('Object detected: %s' % obj[0:11])
                        object = "'%s' varchar(25);" % obj[12:]
                    elif obj[0:15] == 'checkbox-group-':
                        # FOR CHECKBOX GROUPS
                        print('Object detected: %s' % obj[0:14])
                        object = "'%s' varchar(25);" % obj[15:]
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

        status = ''

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
                                status = '[Sibyl Endpoint] Process executed without errors.'
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
        # response = JsonResponse({'response': 'You have reached the writer.', 'status': status}, safe=False)
        # return response

        # Return an HttpResponseRedirect to the Thank You page
        return HttpResponseRedirect('https://marknolledo.pythonanywhere.com/sibyl/thanks')
