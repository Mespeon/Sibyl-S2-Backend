from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import helloWorld

from .models import *

# required to prevent CSRF middleware checks for this particular view
@csrf_exempt
def index(request):
    crossScriptReferencing = helloWorld.sayHello()
    return HttpResponse(crossScriptReferencing)

@csrf_exempt
def login(request):
    return HttpResponse('Login reached. How may I help you?')

@csrf_exempt
def register(request):
    response = HttpResponse()
    hasErrors = False

    # Push the form to the database if a form is submitted to the view.
    # The view will reject the request if no POST form is received.
    if request.method == 'POST':
        # The form itself
        form = request.POST.items()

        # Form data
        # FORMAT - request.POST.get(INPUT_ID_IN_FORM)
        username = request.POST.get('register-username')
        firstName = request.POST.get('register-firstname')
        lastName = request.POST.get('register-lastname')
        password = request.POST.get('register-password')
        confPassword = request.POST.get('conf-register-password')

        #Try pushing values to database/model
        try:
            # Declare an instance of the table to be inserted into/updated.
            thisTable = UserAccount()

            # Assign form values to model values
            thisTable.username = username
            thisTable.first_name = firstName
            thisTable.last_name = lastName
            thisTable.password = password

            # Push and save values
            try:
                thisTable.save()
            except Exception as ex:
                response.write(ex)
                hasErrors = True

        except Exception as ex:
            response.write(ex)
            hasErrors = True

        #Return response depending on results
        if hasErrors == True:
            return response
        else:
            return HttpResponseRedirect('success')

    else:
        return HttpResponse('No form is submitted to this view.')

def regSuccess(request):
    return render(request, 'registry/success.html', {})

#Returns the registration form without a need for CSRF tokens
def register_form(request):
    return render(request, 'registry/register.html', {})
