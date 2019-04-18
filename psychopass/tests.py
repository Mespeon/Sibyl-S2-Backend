from django.test import TestCase
from django.db import connection

import string

# Create your tests here.
def custom_sql():
    with connection.cursor() as cursor:
        try:
            sql = "DROP TABLE IF EXISTS 'nanahira'"
            cursor.execute(sql)
            message = 'Table dropped.'
        except Exception as ex:
            message = ex

    return message

def custom_alter_query():
    with connection.cursor() as cursor:
        try:
            sql = "ALTER TABLE 'testTable' ADD 'comment' varchar(300);"
            cursor.execute(sql)
            message = 'Added specified column.'
        except Exception as ex:
            message = ex

    return message

def custom_create_query(tableName, *args):
    sql = "CREATE TABLE '%s' ('rowId' int NOT NULL, PRIMARY KEY('rowId'));" % tableName
    with connection.cursor() as cursor:
        try:
            # Create the table first
            print('Creating table %s...' % tableName)
            cursor.execute(sql)
            print('Table created.\n\n')

            # Then alter it next
            try:
                print('Altering table...')
                for obj in args:
                    sql_begin = "ALTER TABLE '%s' ADD" % tableName

                    if obj[0:5] == 'text-':
                        print('Object detected: %s' % obj[0:4])
                        object = "'%s' varchar(300);" % obj[5:]
                    elif obj[0:7] == 'select-':
                        print('Object detected: %s' % obj[0:6])
                        object = "'%s' varchar(25);" % obj[7:]
                    elif obj[0:9] == 'textarea-':
                        print('Object detected: %s' % obj[0:8])
                        object = "'%s' varchar(300);" %obj[9:]
                    else:
                        object =''

                    if object != '':
                        sql_final = ' '.join([sql_begin, object])
                        print('Creating column for %s...' % obj)
                        cursor.execute(sql_final)
                        print('Column created.\n\n')

                    status = '\n\nProcess executed without errors.'

            except Exception as ex:
                status = ex

        except Exception as ex:
            status = ex

    return status

# THIS FUNCTION WILL ASSUME A FIXED NUMBER OF FIELDS
# LIKEWISE IN A POST REQUEST WHERE POST.OBJECTS COULD BE COUNTED
# AND ITERATED THROUGH.
def custom_insert_query(tableName, *args):
    pass

def custom_alter_query_multi(tableName, *args):
    print(tableName)

    for obj in args:
        sql_begin = "ALTER TABLE '%s' ADD" % tableName

        if obj[0:5] == 'text-':
            print('Object detected: %s' % obj[0:5])
            object = "'%s' varchar(300);" % obj[5:]
        elif obj[0:7] == 'select-':
            print('Object detected: %s' % obj[0:7])
            object = "'%s' varchar(25);" % obj[7:]
        elif obj[0:9] == 'textarea-':
            print('Object detected: %s' % obj[0:9])
            object = "'%s' varchar(300);" % obj[9:]
        else:
            object = ''

        if object != '':
            sql_final = ' '.join([sql_begin, object])
            print(sql_final, end='\n\n')

        #' '.join([prefix_text, str(store_code)])

def custom_select_query(table):
    with connection.cursor() as cursor:
        try:
            sql = "SELECT * FROM '%s' WHERE rowId = 1" % table
            cursor.execute(sql)
            row = cursor.fetchall()

            if len(row) == 0:
                print('No rows found.')
            else:
                return row

        except Exception as ex:
            return ex

# PARAMS
# custom_create_query(table_name, field01, field02, field03 ... field0n)
#print(custom_create_query('Nanahira', 'text-firstName', 'text-lastName', 'select-gender', 'textarea-comment'))

print(custom_select_query('nanahira'))
