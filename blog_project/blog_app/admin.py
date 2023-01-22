from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #Below are the ways to customize admin interface
    #For created model, Below are some predifined objects to customize admin interface
    list_display=['status','title','slug','author','body','publish','created','updated']  #To display the fields in database
    list_filter=('status','author','created')  #Based on status it will filter the table
    search_fields=('title','body') #IF any word match in title / body it will display that records.
    raw_id_fields=('author',)   #We need to provide id , based on Entered id, it will automatically assign name 
    date_hierarchy='publish' #we can display the data of particular date
    ordering=['status','publish'] #From database table itself we can order table in ascending/desceding. 
    prepopulated_fields= {'slug':('title',)} #To Display slug field automatically, based on someother field(here we using title field).

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']
    list_filter=('active','created','updated')
    search_fields=('name','email','body')
admin.site.register(Post,PostAdmin) 
admin.site.register(Comment,CommentAdmin)