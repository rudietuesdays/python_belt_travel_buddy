from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User

# Create your views here.
def index(request):
    print '*'*20
    print 'List of users objects:', User.objects.all()
    return render(request, 'loginReg_templates/index.html')

def register_user(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm_pw': request.POST['confirm_pw'],
    }

    #pull register method from models.py
    result = User.objects.register_validation(postData)

    #check true or false : user[0] is True, user[1] is false , which comes from the tuple in models.py
    if result[0]:
        print '*'*20
        print result[0], result[1]
        request.session['uid'] = result[1].id
        user_obj = result[1]

        context = {
            'user': user_obj
        }

        return redirect(reverse('travelDash:dashboard'))

    #loop through messages showing errors if the registration wasn't successful
    else:
        for err in range(len(result[1])):
            messages.error(request, result[1][err])
        return redirect('/')

def login_user(request):

    postData = {
        'email': request.POST['login_email'],
        'password': request.POST['login_password'],
    }

    user = User.objects.login_validation(postData)

    print '*'*20
    print user[1]
    if user[0]:
        request.session['uid'] = user[1][0].id
        # request.session['uname'] = user[1][0].first_name
        user_obj = user[1][0]
        context = {
            "user": user_obj
        }
        return redirect(reverse('travelDash:dashboard'))
        # return redirect('/dashboard')
    else:
        for message in range(len(user[1])):
            messages.error(request, user[1][message])
        return redirect('/')

# def dashboard(request):
#     return render(request, 'travelDash_templates/index.html')

def logout_user(request):
    del request.session['uid']
    # del request.session['uname']
    return redirect('/')
