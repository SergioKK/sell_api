import mptt
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Users(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Subcategory(models.Model):
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='Subcategory')

    def __str__(self):
        return self.title


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


mptt.register(Category, order_insertion_by=['title'])


class Items(models.Model):
    users = models.ManyToManyField("Users", related_name="items")
    category = models.ManyToManyField("Category", related_name="items")
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='item_photo', blank=True)
    time_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
