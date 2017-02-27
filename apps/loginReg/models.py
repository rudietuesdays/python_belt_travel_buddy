from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self, postData):
        messages = []
        flag = False

        # no fields can be blank
        if not postData['first_name'] or not postData['last_name'] or not  postData['password'] or not postData['confirm_pw']:
            flag = True
            messages.append('No fields can be blank')

        # is email in correct format
        if not EMAIL_REGEX.match(postData['email']):
            flag = True
            messages.append('Email not valid')

        # names can only be letters
        if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
            flag = True
            messages.append('Name fields may only contain letters')

        # passwords must match
        if postData['password'] != postData['confirm_pw']:
            flag = True
            messages.append('Passwords do not match')

        # password must be at least 8 characters
        if postData['password'] < 8:
            flag = True
            messages.append('Password is too short')

        # email can't already be in database
        users = User.objects.filter(email__iexact=postData['email'])
        if users:
            flag = True
            messages.append('Your email is already in use')

        #if it worked, send the data back to views
        if not flag:
            pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

            user = User.objects.create(first_name= postData['first_name'],
            last_name=postData['last_name'], email=postData['email'],
            password = pw_hash)

            return(True, user)

        else:
            return(False, messages)

    def login_validation(self, postData):
        messages = []
        flag = False

        # must enter an email addres
        if len(postData['email']) < 1:
            flag = True
            messages.append('Please enter your email address')

        # check if the user is in the datebase
        if len(postData['email']) > 0:
            user = User.objects.filter(email=postData['email'])

            if len(user) < 1:
                flag = True
                messages.append('Email not found')
                print 'this is the user: ', user
        else:
            user = False

        # must enter a password
        if len(postData['password']) < 1:
            flag = True
            messages.append('Password too short')

        # if user is found in database, check that hashed passwords match
        if user:
            print "bcrypt result: "
            print (bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password)

            if not bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password:
                flag = True
                messages.append('Password is not valid')

        if flag:
            return (False, messages)
        else:
            return (True, user)

class User(models.Model):
      first_name = models.CharField(max_length=45)
      last_name = models.CharField(max_length=45)
      email = models.EmailField(max_length=45) # EmailField will do validation for us!
      password = models.CharField(max_length=100)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()
