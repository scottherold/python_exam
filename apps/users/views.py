from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..items.models import Item
# Create your views here.

def index(req):
    if 'user_id' in req.session:
        return redirect('users:dashboard')
    else:
        return redirect('users:main')

def create(req):
    if req.method != 'POST':
        return redirect('users:main')
    errors = User.objects.validate(req.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
    else:
        user = User.objects.create_user(req.POST)
        req.session['user_id'] = user.id
    return redirect('users:index')

def update(req, id):
    pass

def delete(req, id):
    pass

def edit(req, id):
    pass

def show(req, id):
    pass

def login(req):
    if req.method != 'POST':
        return redirect('users:main')
    valid, response = User.objects.login(req.POST)
    if valid == True:
        req.session['user_id'] = response
        return redirect("users:index")
    else:
        messages.error(req, response)
    return redirect('users:index')

def logout(req):
    req.session.clear()
    return redirect("users:index")

def main(req):
    return render(req, 'users/main.html')

def dashboard(req):
    user = User.objects.get(id=req.session['user_id'])
    context = {
        'user': user,
        'wishlist_items': Item.objects.filter(user_wishlist__id=user.id).order_by("-updated_at"),
        'other_items': Item.objects.all().exclude(user_wishlist__id=user.id)
    }    
    return render(req, 'users/index.html', context)