from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class Contact(models.Model):
    contact_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    email=models.EmailField(max_length=60)
    phone=models.IntegerField(max_length=13)
    subject=models.CharField(max_length=30)
    message=models.TextField()
    def __str__(self):
        return self.name+'-'+str(self.email)+'-'+self.subject
    
# class Post(models.Model):
#     post_id=models.AutoField(primary_key=True)
#     title=models.CharField(max_length=15)
#     author=models.CharField(max_length=25)
#     content=models.TextField()
#     email=models.EmailField(max_length=60)
#     timestamp=models.DateTimeField(blank=True)
#     def __str__(self):
#         return self.title+' by '+str(self.author)
class Posts(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=25)
    slug=models.CharField(max_length=200)
    content=models.TextField()
    username=models.CharField(null=True, max_length=100)
    views=models.IntegerField(default=0)
    email=models.EmailField(max_length=60)
    timestamp=models.DateTimeField(default=now,blank=True)
    def __str__(self):
        return self.title+' by '+str(self.author)
    
# sno comment user parent blog timestamp
class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    post=models.ForeignKey(Posts, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:36] + ' : comment by ' + self.user.username
    
class Profile(models.Model):
    user=models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    profile_id=models.AutoField(primary_key=True)
    username=models.CharField(null=True, max_length=255)
    bio=models.TextField(null=True)
    image=models.ImageField(null=True, blank=True, upload_to='shop/images')
    website=models.CharField(null=True, blank=True, max_length=255)
    insta=models.CharField(null=True, blank=True, max_length=255)
    linkedin=models.CharField(null=True, blank=True, max_length=255)
    twitter=models.CharField(null=True, blank=True, max_length=255)
    other=models.CharField(null=True, blank=True, max_length=255)
    def __str__(self):
        return str(self.user)   