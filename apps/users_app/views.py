from django.shortcuts import render, HttpResponse, redirect
from .models import User,Message,Comment

from datetime import datetime

# the index function is called when root is visited
def index(request):
    return render(request, "users_app/index.html")

def signin(request):
    return render(request, "users_app/signin.html")

def process_login(request):

    response = User.objects.validate_login_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].first_name
        request.session['full_name'] = response['user'].first_name + ' ' + response['user'].last_name
        request.session['user_id'] = response['user'].id
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        return render(request, "users_app/signin.html")

    return render(request, "users_app/dashboard.html")

def register(request):
    return render(request, "users_app/register.html")

def add_user(request):
    return render(request, "users_app/add_user.html")

def edit_user(request,user_id):
    user_to_edit = User.objects.get(id=user_id)
    context = {
        'user_to_edit'  : user_to_edit
    }
    return render(request, "users_app/edit_user.html",context)

def show_user(request,user_id):
    user_to_show        = User.objects.get(id=user_id)
    this_users_msgs     = Message.objects.filter(to_user=user_id)
    all_comments        = Comment.objects.all()
    current_datetime    = datetime.now()
    print "current_datetime: ",current_datetime

    context = {
        'user_to_show'      : user_to_show,
        'msgs_to_show'      : this_users_msgs,
        'all_comments'      : all_comments,
        'current_datetime'  : current_datetime
    }

    return render(request, "users_app/show_user.html",context)

def profile(request):
    # user in session can edit their own information
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user_to_edit' : this_user
    }
    return render(request, "users_app/edit_profile.html",context)

def process_register(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    response = User.objects.validate_registration_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].first_name
        request.session['full_name'] = response['user'].first_name + ' ' + response['user'].last_name
        request.session['user_id'] = response['user'].id
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        return render(request, "users_app/register.html")

def process_edit_info(request):
    
    response = User.objects.validate_edit_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        user_to_edit = User.objects.get(id=request.POST['user_id'])
        context = {
            'user_to_edit'  : user_to_edit
        }
        return render(request, "users_app/edit_user.html",context)

def process_profile_edit_info(request):
    
    response = User.objects.validate_edit_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        user_to_edit = User.objects.get(id=request.POST['user_id'])
        context = {
            'user_to_edit'  : user_to_edit
        }
        return render(request, "users_app/edit_profile.html",context)

def process_pwd_change(request):
    
    response = User.objects.validate_pwd_change(request.POST)

    if (response['status']):
        request.session['errors']  = []
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        user_to_edit = User.objects.get(id=request.POST['user_id'])
        context = {
            'user_to_edit'  : user_to_edit
        }
        return render(request, "users_app/edit_user.html",context)

def process_profile_pwd_change(request):
    
    response = User.objects.validate_pwd_change(request.POST)

    if (response['status']):
        request.session['errors']  = []
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        user_to_edit = User.objects.get(id=request.POST['user_id'])
        context = {
            'user_to_edit'  : user_to_edit
        }
        return render(request, "users_app/edit_profile.html",context)

def process_profile_desc_change(request):
    
    response = User.objects.validate_desc_change(request.POST)

    if (response['status']):
        request.session['errors']  = []
        return redirect('/dashboard')
    else:
        request.session['errors'] = response['errors']
        user_to_edit = User.objects.get(id=request.POST['user_id'])
        context = {
            'user_to_edit'  : user_to_edit
        }
        return render(request, "users_app/edit_profile.html",context)

def process_message(request):

    response = Message.objects.validate_message_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        redirect_str = '/show/' + str(request.POST['msg_for'])
        return redirect(redirect_str,request.POST['msg_for'])
    else:
        request.session['errors'] = response['errors']
        user_to_show = User.objects.get(id=request.POST['msg_for'])
        context = {
            'user_to_show'  : user_to_show
        }
        return render(request, "users_app/show_user.html",context)

def process_comment(request):

    response = Comment.objects.validate_comment_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        redirect_str = '/show/' + str(request.POST['comment_for'])
        return redirect(redirect_str,request.POST['comment_for'])
    else:
        request.session['errors'] = response['errors']
        user_to_show = User.objects.get(id=request.POST['msg_for'])
        context = {
            'user_to_show'  : user_to_show
        }
        return render(request, "users_app/show_user.html",context)

def dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    other_users = User.objects.all().exclude(id=request.session['user_id'])

    context = {
        'this_user'     : this_user,
        'other_users'   : other_users
    }

    return render(request, 'users_app/dashboard.html', context)  

def logoff(request):
    request.session['name'] = ""
    return redirect('/')