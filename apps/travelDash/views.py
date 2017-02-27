from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Trip, User, UserTrip

# Create your views here.

def index(request):
    user = User.objects.get(id=request.session['uid'])
    myTrips = Trip.objects.filter(user__id=request.session['uid'])
    tripsIJoined = UserTrip.objects.filter(user__id=request.session['uid'])
    otherTrips = Trip.objects.exclude(user__id=request.session['uid'])&Trip.objects.exclude(trip_joined__user__id=request.session['uid'])
    context = {
        'user': user,
        'myTrips': myTrips,
        'otherTrips': otherTrips,
        'tripsIJoined': tripsIJoined,
    }

    print 'joined trips:', UserTrip.objects.filter(user_id=request.session['uid'])

    return render(request, 'travelDash_templates/index.html', context)

def add_plan_page(request):

    return render(request, 'travelDash_templates/add_plan.html')


def add_plan(request):
    postData = {
        'destination': request.POST['destination'],
        'description': request.POST['description'],
        'start_date': request.POST['start_date'],
        'end_date': request.POST['end_date'],
        'user_id': request.session.get('uid')
    }

    result = Trip.objects.validation(postData)

    if result[0]:
        return redirect(reverse('travelDash:dashboard'))

    else:
        for err in range(len(result[1])):
            messages.error(request, result[1][err])
        return redirect(reverse('travelDash:add_plan'))

def view_destination(request, id):
    destination = Trip.objects.get(id=id)
    user_id=destination.user.id
    thisTrip = UserTrip.objects.filter(trip__id=id)&UserTrip.objects.exclude(user__id=user_id)#&UserTrip.objects.exclude(user__id=user_id)
    print thisTrip
    context = {
        'thisTrip': thisTrip,
        'destination': destination,
        'uid': request.session['uid'],
    }
    print user_id
    return render(request, 'travelDash_templates/destination.html', context)

def join_trip(request, id):
    user = User.objects.get(id=request.session['uid'])
    trip = Trip.objects.get(id=id)
    vacation = UserTrip.objects.create(user_id=user.id, trip_id=trip.id)
    return redirect(reverse('travelDash:dashboard'))
