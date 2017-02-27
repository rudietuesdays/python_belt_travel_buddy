from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from ..loginReg.models import User

# Create your models here.
class TripManager(models.Manager):
    def validation(self, postData):
        messages=[]
        flag = False

        # no field can be blank
        if not postData['destination'] or not postData['description'] or not postData['start_date'] or not postData['end_date']:
            flag = True
            messages.append('No fields can be blank')

        # start date must be in future and end date must be after start date
        if not postData['start_date'] or not postData['end_date']:
            flag = True
            messages.append('You must enter a start and end date')
        else:
            if postData['start_date']:
                start_date_obj = datetime.strptime(postData['start_date'], '%Y-%m-%d')
                print '*'*20
                print start_date_obj, type(start_date_obj)
                print datetime.now(), type(datetime.now())
            if postData['end_date']:
                end_date_obj = datetime.strptime(postData['end_date'], '%Y-%m-%d')

            if start_date_obj < datetime.now():
                flag = True
                messages.append('All trips must start on a future date, not in the past')

            if start_date_obj > end_date_obj:
                flag = True
                messages.append('Travel end date cannot be before start date')

        if not flag:
            print postData['user_id']
            trip = Trip.objects.create(destination= postData['destination'],
            description=postData['description'], start_date=postData['start_date'], end_date=postData['end_date'], user_id=postData['user_id'])
            return (True, trip)

        else:
            return(False, messages)


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class UserTrip(models.Model):
    user = models.ForeignKey(User, related_name='user_joined')
    trip = models.ForeignKey(Trip, related_name='trip_joined')
    date_added = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
