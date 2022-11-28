from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

#This code is for the login page
context = {}
def index(request):
    return render(request, 'index.html', context=context)

def login_view(request):
    if not request.POST.get('username') or not request.POST.get('password'):
        return render(request, 'index.html', context=context)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('admin:index') # Allow access to the admin interface
    else:
        return render(
            request, 'index.html', {
                    'error_message': 'Login Failed! \
                    Please enter Valid Username and Password.', })

# Methods for custom error handlers that serve htmls in templates/home/errors
def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response

def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response
