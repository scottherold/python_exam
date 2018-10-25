from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from ..users.models import User

# Create your views here.

def index(req):
    pass

def create(req):
    return render(req, 'items/create.html')

def update(req, id):
    pass

def destroy(req, id):
    if req.method != 'POST':
        return redirect('users:index')
    else:
        Item.objects.delete_item(id)
    return redirect('users:index')

def new(req):
    if req.method != 'POST':
        return redirect('items:create')
    errors = Item.objects.validate(req.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
        return redirect('items:create')
    else:
        Item.objects.create_item(req.POST)
    return redirect('users:index')

def edit(req, id):
    pass

def show(req, id):
    context = {
        'item': Item.objects.get(id=id),
        'users': User.objects.filter(wishlist_item__id=id)
    }
    return render(req, 'items/show.html', context)

def remove(req, id):
    if req.method != 'POST':
        return redirect('users:index')
    else:
        Item.objects.remove_item(id, req.POST)
    return redirect('users:index')

def add(req, id):
    if req.method != 'POST':
        return redirect('users:index')
    else:
        Item.objects.add_wishlist_item(id, req.POST)
    return redirect('users:index')