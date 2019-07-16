from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
import mptt
from mptt.models import MPTTModel, TreeForeignKey


class Users(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])


mptt.register(Category, order_insertion_by=['title'])


@python_2_unicode_compatible
class Items(models.Model):
    users = models.ManyToManyField(User, related_name="Users")
    category = models.ManyToManyField(Category, related_name="Category")
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='item_photo', blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    visit_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('price', 'time_added', 'visit_count')

    def __str__(self):
        return self.title

    def add_visit(self):
        if self.visit_count is not None:
            self.visit_count += 1
        else:
            self.visit_count = 0
