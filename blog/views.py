from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.
def index(request):
    my_post=Blogpost.objects.all()
    print(my_post)
    
    return render(request,'blog/index.html',{'my_post':my_post})

def blogpost(request,id):
    my_post=Blogpost.objects.all()
    post=Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return render(request,'blog/blogpost.html',{'post':post,'my_post':my_post})