from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime
from django.utils import timezone

def get_time_now():
    # return datetime.datetime.today()
    dt = datetime.datetime.now()
    return datetime.datetime(dt.year, dt.month, dt.day)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def register_validate(self, postData):
        context = {
            'error_message' : [],
            'success_message' : []
        }
        email = postData['email']
        if not EMAIL_REGEX.match(email):
            context['error_message'].append('ERROR: Invalid Email Address!')

        name_check = postData['name']
        if len(name_check) < 3:
            context['error_message'].append('ERROR: Name must be at least 2 characters!')

        alias = postData['alias']
        if len(name_check) < 3:
            context['error_message'].append('ERROR: Name must be at least 2 characters!')

        password_in = postData['password']
        if len(password_in) < 8:
            context['error_message'].append('ERROR: Password must be at least 8 characters!')

        password_confirm = postData['password_confirm']
        if password_in != password_confirm:
            context['error_message'].append('ERROR: Password confirmation failed!')

        if not postData['dob'] or len(postData['dob']) < 1:
            context['error_message'].append(
                'ERROR: Please enter your Date Of Birth!')
        else:
            first_date= datetime.datetime.strptime(str(postData['dob']),'%Y-%m-%d')
            date_now = get_time_now()
            if date_now < first_date:
                context['error_message'].append(
                    'ERROR: You can\'t be born in the future!')

        #now test to see if user exists for email
        check = User.objects.filter(email=email)
        if check:
            context['error_message'].append('ERROR: User already exists!')

        if not context['error_message'] == []:
            return context
        else:
            user = User.objects.create(
                name=name_check,
                alias=alias,
                email=email,
                dob=postData['dob'],
                password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()),
            )
            user.save()
            context['success_message'].append('SUCCESS: User Registered!')
            context['user'] = user
            return context

    def login_validate(self, postData):

        context = {
            'error_message' : [],
            'success_message' : []
        }

        email = postData['email']
        if not EMAIL_REGEX.match(email):
            context['error_message'].append('ERROR: Invalid Email Address!')

        password_in = postData['password']
        if len(password_in) < 8:
            context['error_message'].append('ERROR: Password must be at least 8 characters!')

        #now test to see if user exists for email
        try:
            user = User.objects.get(email=email)
        except:
            user = False
            context['error_message'].append('ERROR: User does not exist!')

        if user != False:
            if user.password != bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
                context['error_message'].append('ERROR: Password does not match!')

        if not context['error_message'] == []:
            return context
        else:
            context['success_message'].append('SUCCESS: User Logged In!')
            context['user'] = user
            return context

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dob = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    objects = UserManager()
