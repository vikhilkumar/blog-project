#Session - 91
from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog_app.forms import EmailSendForm,CommentForm
from taggit.models import Tag

# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:               #tagging session - 98
        tag=get_object_or_404(Tag,slug=tag_slug)  #Tag is model name created while TaggableManager()-taggit
        post_list=post_list.filter(tags__in=[tag])
    #pagination concept (session - 93)
    paginator=Paginator(post_list,2)  #each page only 2 post will display
    page_number=request.GET.get('page')   #page is inbuilt parameter- it gives us page number
    try:
        post_list=paginator.page(page_number) #when we hit the url it gives the page no-none, so it throws PageNotAnInteger
    except PageNotAnInteger:
        post_list=paginator.page(1)   #So we manually giving the pageNo to display first page
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog_app/post_list.html',{'post_list':post_list})

#Pagination using Class based views
from django.views.generic import ListView
class PostListView(ListView):
    model=Post
    paginate_by=2


def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
       #Above line meaning .. I want to get particular post details based on year,month,day and post. I will provide above info based on
            #  above info ,get corresponding post and send that post object to post_detail.html page.
    #employee(-modelname)=get_list_or_404(employee,eno=101)

    return render(request,'blog_app/post_detail.html',{'post':post})



def post_details(request,id):
    post=Post.objects.get(id=id)
    comments=post.comments.filter(active=True) #For understanding have a look in models.py
                  #above object retrives the comments which are active only.  comments is related_name used in models.py
    csubmit=False
    if request.method=='POST': #If enduser enters the data and click on submit button POST action will be done , otherwise else action. Initially when url hits else will be execured once we click on submit button if we execute
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)  #Stores the enduser comments in new_comment but wont save in database
            new_comment.post=post   #storing post(line 40) data in post field, it will create new filed with post in Post model and store the data in Post model.
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'blog_app/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})
          
          #{%with comments.count as comments_count%} {{coments_count|pluralize}} #if 1 comment it will display comment otherwise comments.

from django.core.mail import send_mail

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data  #it will store the user entered data in dict form
            #send_mail('subject','message','From',[To])
            print(id)
            mailsendview_url='mailsendview/'+str(id)
            print(mailsendview_url)
            post_url=request.build_absolute_uri(mailsendview_url) # generates full url
            print('post_url:',post_url)
            send_mail('subject','message','vikhilkumartesting@gmail.com',[cd['To']])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog_app/sharebymail.html',{'form':form,'post':post,'sent':sent})