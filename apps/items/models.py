from django.db import models
from ..users.models import User

# Create your models here.

class ItemManager(models.Manager):
    def validate(self, form):
        errors = []
        if len(form['item_name']) == 0:
            errors.append('Item or Product must have a name')
        if len(form['item_name']) > 0 and len(form['item_name']) < 3:
            errors.append('Item or Product name must be at least three characters long')
        return errors

    def create_item(self, item_data):
        current_user = User.objects.get(id=item_data['user_id'])
        item = self.create(item_name=item_data['item_name'], user_added=current_user)
        item.user_wishlist.add(current_user)

    def delete_item(self, id):
        self.get(id=id).delete()

    def remove_item(self, id, user_data):
        current_user = User.objects.get(id=user_data['user_id'])
        self.get(id=id).user_wishlist.remove(current_user)

    def add_wishlist_item(self, id, user_data):
        current_user = User.objects.get(id=user_data['user_id'])
        self.get(id=id).user_wishlist.add(current_user)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    user_added = models.ForeignKey(User, related_name="added_item", on_delete=models.DO_NOTHING)
    user_wishlist = models.ManyToManyField(User, related_name="wishlist_item")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = ItemManager()