from time import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

# Session - 90
# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))   #For dropdown choices
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    title=models.CharField(max_length=256)
    slug=models.CharField(max_length=264,unique_for_date='publish')  #We need to give publish in the url call in search engine operation(chrome). so our site will recommend in top10
    author=models.ForeignKey(User,models.CASCADE,related_name='blog_posts')  #Whatever the post published by that user, we will get all posts(User.blog_post)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)  #gets current time
    created=models.DateTimeField(auto_now_add=True)  #When post got created it will take that time
    updated=models.DateTimeField(auto_now=True) #when we update post it will give that particular time.
    objects=CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)   #will sort in descending order

    def __str__(self):
        return self.title    #If we are going to Publish our post, then it will just display title.

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
    
#Model related to comments section - Session 96
class Comment(models.Model):
    post=models.ForeignKey(Post,models.CASCADE,related_name='comments') #Above Post model , primary key column will be available to this comment model
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True) #If we want to delete the comment

    class Meta:
        ordering=('-created',)   #display recently created comment to old .
    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)

