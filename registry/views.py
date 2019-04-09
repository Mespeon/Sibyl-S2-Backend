from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    return HttpResponse('You have reached the Registry Django app from the outside.')

@csrf_exempt    # required to prevent CSRF middleware checks for this particular view
def register(request):
    if request.method == 'POST':
        form = request.POST.items()
        # FORMAT
        # request.POST.get(INPUT_ID_IN_FORM)
        username = request.POST.get('register-username')
        firstName = request.POST.get('register-firstname')
        lastName = request.POST.get('register-lastname')
        password = request.POST.get('register-password')
        confPassword = request.POST.get('conf-register-password')

        # if form.is_valid():
        #     return HttpResponse('Form is valid.')
        # else:
        #     return HttpResponse('Form is invalid.')
        response = HttpResponse()
        response.write('Name entered: ' + firstName + ' ' + lastName + '<br/>')
        response.write('Username entered: ' + username + '<br/>')
        response.write('Password entered: ' + password + '<br/>')
        if password == confPassword:
            response.write('<i>Passwords match.</i><br/>')
        else:
            response.write('<i>Passwords do not match.</i><br/>')

        return response
#Returns the registration form without a need for CSRF tokens
@csrf_exempt
def register_form(request):
    return render(request, 'registry/register.html', {})
