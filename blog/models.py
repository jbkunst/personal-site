from django.db import models
from django.contrib.sitemaps import ping_google
from random import randrange
import datetime

class Category(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) 

    def counter(self):
        return self.post_set.all().count()
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('category', [str(self.slug)])
    
class Post(models.Model):

    STATUS_CHOICES = ((1, 'Live'), (2, 'Draft'))

    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
 
    def save(self, force_insert=False, force_update=False):
        super(Post, self).save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            pass
        
    def get_categories(self):
        return self.category.all()
 
    class Meta:
        ordering = ('-pub_date',)
           
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('post', [str(self.slug)])