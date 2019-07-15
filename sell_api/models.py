from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from hitcount.models import HitCount, HitCountMixin


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
class Items(models.Model, HitCountMixin):
    users = models.ManyToManyField(User, related_name="Users")
    category = models.ManyToManyField(Category, related_name="Category")
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='item_photo', blank=True)
    time_added = models.DateTimeField(default=timezone.now)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ('-price', '-time_added')

    def __str__(self):
        return self.title
