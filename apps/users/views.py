from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt
import datetime


def index(request):
    return render(request, 'users/index.html')

def verify(request):
    if len(request.POST['name']) == 0  or len(request.POST['user_name']) == 0 or len(request.POST['confirm_pw']) == 0 or len(request.POST['password']) == 0:
        messages.error(request, 'All fields must be filled out!')
        return redirect ('/')
    if not request.POST['name'].replace(' ','').isalpha():
        messages.error(request,'First and Last names can only contain letters!')
        return redirect ('/')
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request,'Passwords must match!')
        return redirect ('/')
    if len(request.POST['password']) < 8:
        messages.error(request,'Passwords must be at least 8 characters long!')
        return redirect ('/')
    # if request.POST['password'].isdigit:
    #     messages.error(request,'Passwords cannot contain numbers!')
    #     return redirect ('/')

    password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    new_user = User.objects.create(name= request.POST['name'], username = request.POST['user_name'], password = password_hash)
    request.session['id'] = new_user.id
    request.session['name'] = new_user.name
    return redirect('/travels')

def login(request):
    user = User.objects.filter(username = request.POST['user_name'])
    request.session['name'] = user[0].name
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            return redirect('/travels')
        else:
            messages.error(request, 'Username/Password invalid')
            return redirect('/')
    else:
        messages.warning(request, 'User not found')
    return redirect('/') 

def travels(request):
    trips = Trip.objects.all()
    # my_trip = Trip.objects.get(id = 1)
    # self_trips = my_trip.trips.all()
    # user_id = User.objects.get(id = )
    # self_trips = Trip.objects.users.get(id = request.session['id'])
    # others_trip = Trip.objects.all()
    context = {
        "trips": trips,
        # "others_trip": others_trip
    }
    return render (request, 'users/travels.html', context)

def add_trip(request):
    
    return render(request, 'users/add_trip.html')

def process(request):
    
    # need validations!
    new_trip = Trip.objects.create(destination = request.POST['destination'], plan = request.POST['description'], start_date = request.POST['date_from'], end_date = request.POST['date_to'])
    print (new_trip.id)
    print (request.session['id'])
    user = User.objects.get(id = request.session['id'])
    new_trip[0].id = request.session['new_trip']
    this_trip = Trip.objects.get(id = new_trip.id)
    this_trip.users.add(user)
    
    return redirect('/travels')

def destination_page(request, number):
    trip = Trip.objects.filter(id = number)
    context = {
        "trip": trip
    }
    return render(request, 'users/destination_page.html', context)
def logout(request):
    del request.session
    return redirect('/')
