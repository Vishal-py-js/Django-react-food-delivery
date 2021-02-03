from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    slug = models.SlugField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("food:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("food:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("food:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total
    
    @property
    def get_slug(self):
        slug = self.item.slug
        return slug


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f"{self.user.username}'s order'"

    @property
    def get_cart_total(self):
        orderitems = self.items_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.items_set.all()
        total = sum([item.quantity for item in orderitems])
        return total