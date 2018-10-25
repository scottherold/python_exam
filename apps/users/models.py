from __future__ import unicode_literals
from django.db import models
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def validate(self, form):
        errors = []
        if len(form['name']) < 3:
            errors.append('Name must be at least three characters long')
        if len(form['name']) < 3:
            errors.append('Name must be at least three characters long')
        try:
            self.get(user_name=form['user_name'])
            errors.append('Username already taken, please choose a different one!')
        except:
            pass
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        if form['password'] != form['password_confirm']:
            errors.append('Password confirmation must match password')
        return errors

    def create_user(self, user_data):
        pw_hash = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())

        user = self.create(
            name=user_data['name'],
            user_name=user_data['user_name'],
            pw_hash=pw_hash,
            hire_date=user_data['hire_date']
        )
        return user

    def login(self, form):
        user_list = self.filter(user_name=form['user_name'])
        if len(user_list) > 0:
            user = user_list[0]
            if bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
                return (True, user.id)
            else:
                return (False, "Incorrect Username and Password Combination")
        else:
            return (False, "Incorrect Username and Password Combination")

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()