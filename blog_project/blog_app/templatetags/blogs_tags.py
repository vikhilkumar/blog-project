#Session - 99

from atexit import register
from blog_app.models import Post
from django import template
register=template.Library()

@register.simple_tag
def total_posts():    #To use this filter we need to use this function name in html file.
    return Post.objects.count()  #returns number of posts

@register.inclusion_tag('blog_app/latest_posts.html')
def show_latest_posts():
    latest_posts=Post.objects.order_by('-publish')[:3]
    return {'latest_posts':latest_posts}

from django.db.models import Count
@register.assignment_tag
def get_most_commented_post(count=5):
    return  Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
                  #annonate will assign the count value of comments to total_comments variable and new column will be created by default.
    
