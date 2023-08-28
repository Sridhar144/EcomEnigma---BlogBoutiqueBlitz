from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from .models import Contact,Posts, BlogComment, Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog.templatetags import extras
from django.views import generic

from django.views.generic import DetailView
from django.urls import reverse_lazy
# Create your views here.
# page backends
def index(request):
    allposts=Posts.objects.all().order_by('-views')[:2]
    orderposts=Posts.objects.all().order_by('-timestamp')[:3]
    context={'allposts':allposts, 'orderposts':orderposts}

    print(context)
    return render(request, 'blog/index.html', context)
def about(request):
    return render(request,'blog/about.html')
def blogger(request):
    allposts=Posts.objects.all()
    context={'allposts':allposts}
    return render(request,'blog/blogger.html', context)

def contact(request):
    messages.info(request,'Contact Me')
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        subject=request.POST.get('subject','')
        message=request.POST.get('message','')
        if len(name)<2 or len(email)<5 or len(phone)<6 or len(subject)<5:
            messages.error(request,'Please enter the details appropriately!')
        else:
            contact=Contact(name=name, email=email, phone=phone, subject=subject, message=message)
            contact.save()
            messages.success(request, 'Your form has been submitted correctly!')
    return render(request,'blog/contacts.html')
def blogpost(request, slug):
    #return HttpResponse(f"This is the blogpost:{slug}")
    post=Posts.objects.filter(slug=slug).first()
    post.views+=1
    usern=post.username
    post.save()
    print(usern)
    userna=Profile.objects.filter(username=usern).first()
    print(userna)
    pid=userna.profile_id
    print(pid)
    comments=BlogComment.objects.filter(post=post, parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replydict={}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]=[reply]
        else:
            replydict[reply.parent.sno].append(reply)
    context={'post':post, 'comments':comments, 'user':request.user, 'replydict':replydict, 'pid':pid, 'userna':userna}
    return render(request,'blog/blogpost.html',context)
    

def postcomment(request):
    #return HttpResponse(f"This is the blogpost:{slug}")
    if request.method=='POST':
        # sno=request.POST.get('sno')
        comment=request.POST.get('comment')
        user=request.user
        postSno=request.POST.get('postSno')
        post=Posts.objects.get(post_id=postSno)
        parentSno=request.POST.get('parentSno')
        if parentSno == "":
            comment=BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully!")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment, user=user, post=post, parent=parent)
            
            comment.save()
            messages.success(request, f"Your have replied to {user.username}!")

    return redirect(f"/blog/{post.slug}")

def search(request):
    query=request.GET['query']
    allpoststitle=Posts.objects.filter(title__icontains=query)
    allpostscontent=Posts.objects.filter(content__icontains=query)
    allpostsauthor=Posts.objects.filter(author__icontains=query)
    allposts=allpoststitle.union(allpoststitle,allpostscontent,allpostsauthor)
    if len(query)>80:
        allposts=[]
    context={'allposts':allposts, 'dotell':"", 'query':query}
    if not len(allposts):
        context['dotell']="Query not set properly, Please search appropriate phrase to search for an item"
    

    return render(request, 'blog/search.html', context)
# authenticate API'S work
def handlesignup(request):
    if request.method=='POST':
        #get post parqmeters
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        bio=request.POST['bio']
        website=request.POST['website']
        insta=request.POST['insta']
        linkedin=request.POST['linkedin']
        twitter=request.POST['twitter']
        other=request.POST['other']

        #no errors part
        if len(username)>12:
            messages.warning(request, "Your username must be under 12 characters. Please create an appropriate one")
            return redirect('bloghome')
        count_uup=0
        for s in username:
            if s.isupper():
                count_uup+=1
                break
            
        if not username.isalnum() or count_uup != 0:
            messages.warning(request, "Your username must be alphanumeric and lowecase only! Please create an appropriate one")
            return redirect('bloghome')
        if pass1!=pass2:
            messages.warning(request, "Your passwords dont match. Please enter same password for verification")
            return redirect('bloghome')
            print(pass1)
        count_pnum=0
        count_pal=0
        for s in pass1:
            if s.isnumeric():
                count_pnum+=1
            if s.isalpha():
                count_pal+=1
        if not count_pal and not count_pnum:
            messages.warning(request, "Password criteria not match. Please enter password with alphabets and numbers")
            return redirect('bloghome')
            
        # create user
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        profile=Profile(username=username,bio=bio, website=website,insta=insta, linkedin=linkedin, twitter=twitter, other=other)
        profile.save()
        messages.success(request, "Your account has been created successfully")
        return redirect('/blog')
    else:
        return HttpResponse('404 - Not found')
def userlogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In!")
            return redirect("bloghome")
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect("bloghome")
    return HttpResponse('ERROR 404-not found')

def userlogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("/blog")
def profile(request):
    
    user = request.user
    theuser=Profile.objects.filter(username=user).first()
    print(user, theuser)
    pid=theuser.profile_id
    print(pid)
    return render(request, 'blog/profile.html',{'user':user, 'pid':pid})
class ShowProfile(DetailView):
    model=Profile
    template_name='blog/user_profile.html'
    def get_context_data(self,*args,**kwargs):
        profile=Profile.objects.all()
        print(profile)
        context=super(ShowProfile, self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(Profile, profile_id=self.kwargs['pk'])
        context['page_user']=page_user
        return context
def make(request):
    print(request.user.email)
    if request.method=='POST':
        title=request.POST.get('title','')
        all_words = title.split()
        slug=all_words[0]
        author=request.POST.get('author','')
        content=request.POST.get('content','')
        username=request.POST.get('username','')
        email=request.user.email
        print(title,author,content,username,email)
        post=Posts(title=title, slug=slug,author=author, content=content, username=username, email=email)
        post.save()
        messages.success(request, "Successfully posted blogpost!")

    return render(request, 'blog/make_blog.html')
