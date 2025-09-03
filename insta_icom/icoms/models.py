from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    choice=[
        ('image','image'),
        ('video','video'),
    ]
    title=models.CharField(max_length=100)
    desc=models.TextField()
    type=models.CharField(max_length=100,choices=choice)
    image=models.FileField(upload_to='postimage/')
    video=models.FileField(upload_to='postvideo/',null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    desc=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to="profile_image/",null=True,blank=True)
    following_count=models.PositiveIntegerField(default=0,null=True,blank=True)
    followers_count=models.PositiveIntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return str(self.user)  if self.user else "No User"
class Reels(models.Model):
    image=models.ImageField(upload_to='reels_image',null=True,blank=True)
    captions=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    video=models.FileField(upload_to="reels_video",null=True,blank=True)
    def __str__(self):
        return f'{self.captions}-{self.date}'

class Comments(models.Model):
    comments_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True ,related_name="other_user")
    reply_comments=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="own_user")
    message=models.TextField(null=True,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    datetime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return f"{self.comments_user.username}-{self.message}"
class Follow_user(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following_user")
    followers=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers_user")
    datatime=models.DateTimeField(auto_now=True,null=True,blank=True)
    def __str__(self):
        return f"{self.followers.username} followed by {self.following.username}"
class Message(models.Model):
    ruser=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    other=models.ForeignKey(User,on_delete=models.CASCADE,related_name="otheruser")
    image=models.ImageField(upload_to="mimage")
    video=models.FileField(upload_to="mvideo",null=True,blank=True)
    datetime=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    msg=models.TextField(null=True,blank=True)
    def __str__(self):
        return f"req_user - {self.ruser.username} - other- {self.other.username}"
    



