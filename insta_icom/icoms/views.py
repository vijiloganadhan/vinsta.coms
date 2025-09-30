from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Post,Profile,Reels,Comments,Follow_user,Message
from django.contrib.auth import authenticate,login,logout
import random
from django.db.models import Q ,F
from cloudinary.uploader import upload
# Create your views here

def signup_views(request):
    msg = ''
    if request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        user = request.POST.get('user')
        email = request.POST.get('email')
        p1 = request.POST.get('p1')
        p2 = request.POST.get('p2')

        if p1 == p2:
            if not User.objects.filter(username=user).exists():
                User.objects.create_user(username=user, email=email, password=p1)
                return redirect('login')
            else:
                msg = "Username already exists"
        else:
            msg = "Passwords do not match"

    context = {
        'msg': msg
    }
    return render(request, 'signup.html', context)

def login_views(request):
    msg=''
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        name=request.POST.get('user')
        p1=request.POST.get('p1')
        user=authenticate(request,username=name,password=p1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            msg="invalid creditials"
    context={
        'msg':msg
    }
    return render(request,'login.html',context)
def logout_views(request):
    logout(request)
    return redirect('home')
def createuserprofile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method =="POST":
        name=request.POST.get("name")
        desc=request.POST.get("desc")
        image=request.FILES.get('image')
        if name:
            Profile.objects.create(name=name,desc=desc,image=image,user=request.user)
            return redirect('home')
    return render(request,'createprofile.html')
def user_profile(request,ids):
    profile=get_object_or_404(Profile,id=ids,user=request.user)
    post=Post.objects.filter(user=request.user)
    following=User.objects.filter(following_user__followers=request.user)
    followers=User.objects.filter(followers_user__following=request.user)
    reels=Reels.objects.filter(user=request.user)
    context={
        'profile':profile,
        'post':post,
        'following':following,
        'followers':followers,
        'reels':reels
    }
    return render(request,'userprofiledetails.html',context)

def target_profile(request,ids):
    profile_user=get_object_or_404(User,id=ids)
    profile=get_object_or_404(Profile,user=profile_user)
    post=Post.objects.filter(user=profile_user)
    is_following = request.user.is_authenticated and Follow_user.objects.filter(following=profile_user, followers=request.user).exists()
    context={
        'profile_user':profile_user,
        'profile':profile,
        'post':post,
        'is_following':is_following,
    }
    return render(request,'profileview.html',context)
def follow(request,ids):
    target_user=get_object_or_404(User,id=ids)
    if request.user !=target_user and not Follow_user.objects.filter(following=target_user,followers=request.user).exists():
        Follow_user.objects.create(following=target_user,followers=request.user)
        profile=Profile.objects.filter(user=target_user).update(followers_count=F('followers_count')+1)
        profile=Profile.objects.filter(user=request.user).update(following_count=F('following_count')+1)
    return redirect('profileview',ids=ids)
def unfollow(request,ids):
    target_user=get_object_or_404(User,id=ids)
    if request.user !=target_user:
        follow=Follow_user.objects.filter(following=target_user,followers=request.user)
        follow.delete()
        profile=Profile.objects.filter(user=target_user).update(followers_count=F('followers_count')-1)
        profile=Profile.objects.filter(user=request.user).update(following_count=F('following_count')-1)
    return redirect('profileview',ids=ids)


def homes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile=Profile.objects.filter(user=request.user).first()
    if profile:
        pro=profile
    else:
        pro="user profile "
    if Follow_user:
       follower_users = User.objects.filter(following_user__followers=request.user)
    reels=list(Reels.objects.order_by("-date")[:5])
    random.shuffle(reels)
    context={
        'post':Post.objects.all().order_by('-id'),
        'profile':pro,
        'comments':Comments.objects.all().order_by("-id"),
        'followers':follower_users,
        'reels':reels
    }
    return render(request,'home.html',context)

def edit_user_profile(request,ids):
    profile=get_object_or_404(Profile,user=request.user)
    if request.method=="POST":
        name=request.POST.get("name")
        desc=request.POST.get("desc")
        image=request.FILES.get("image")
        profile.name=name
        profile.desc=desc
        profile.image=image
        profile.save()
        return redirect("userprofiledetails" ,ids=profile.id)
    context={
        'profile':profile
    }
    return render(request,'editprofile.html',context)        

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        title=request.POST.get('title')
        desc=request.POST.get('desc')
        choice=request.POST.get('choice')
        image=request.FILES.get('images')
        video=request.FILES.get('videos')
        image_url=None
        video_url=None
        if image:
            image_url = upload(image, resource_type="image")['secure_url']
        if video:
            video_url= upload(video , resource_type="video")["secure_url"]

        Post.objects.create(title=title,desc=desc,type=choice,image=image_url,video=video_url,user=request.user)
        return redirect('home')
    return render(request,'create_post.html')


def search(request):
    user=""
    msg=""
    if request.method=="POST":
        query=request.POST.get('q')
        if query:
             user=Profile.objects.filter(user__username__contains=query).exclude(user=request.user)
             if not user:
                 msg="user not found"
        else:
            msg=" query not given "
    context={
        'profile':user ,
        'msg':msg
    }
    return render(request,'search.html',context)
def post_view(request,ids):
    user_post=Post.objects.filter(id=ids,user=request.user)
    context={
        'userpost':user_post
    }
    return render(request,'postviews.html',context)
def post_delete(request,ids):
    post_user=Post.objects.filter(id=ids,user=request.user)
    post_user.delete()
    return redirect('home')

def reels_upload(request):
    if request.method=="POST":
        captions=request.POST.get('captions')
        image=request.FILES.get('image')
        video=request.FILES.get('video')
        Reels.objects.create(captions=captions,image=image,user=request.user,video=video)
        return redirect('reels')
    return render(request,'upload_reels.html')
def watch_reels(request):
    # reels = Reels.objects.order_by('?')[:5]  # Get 10 random reels
    reels=list(Reels.objects.all().order_by("-id"))
    random.shuffle(reels)
    context={
        'reels': reels
    }
    return render(request,'reels.html',context)



def comments_user(request, ids):
    if not request.user.is_authenticated:
        return redirect("login")

    post = get_object_or_404(Post, id=ids)
    current_user = request.user

    # Determine the other user in the chat (person you're talking to)
    if current_user == post.user:
        # If current user is post owner, check latest message
        latest_comment = Comments.objects.filter(post=post).exclude(comments_user=current_user).first()
        other_user = latest_comment.comments_user if latest_comment else None
    else:
        other_user = post.user

    # On POST - create message
    if request.method == "POST":
        msg = request.POST.get("msg")
        if msg and other_user:
            Comments.objects.create(
                post=post,
                comments_user=current_user,
                reply_comments=other_user,
                message=msg
            )
            return redirect("comments", ids=ids)

    # Show all messages between these two users for this post
    chat = Comments.objects.filter(
        post=post
    ).filter(
        (Q(comments_user=current_user, reply_comments=other_user) |
         Q(comments_user=other_user, reply_comments=current_user))
    ).order_by("datetime")

    context = {
        "chat": chat,
        "post": post,
        "other_user": other_user
    }
    return render(request, 'comments.html', context)

def post_search(request):
    search_post=[]
    msg=""
    if request.method=="POST":
        title=request.POST.get("title")
        if title:
            search_post=Post.objects.filter(title__icontains=title)
        else:
            msg="enter post title here "
    context={
        'post_search':search_post
    }
    return render(request,'search_post.html',context)
def message_with_others(request, ids):
    if not request.user.is_authenticated:
        return redirect("login")

    other = get_object_or_404(User, id=ids)

    if request.method == "POST":
        msg = request.POST.get("msg")
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        if msg or image or video:
            Message.objects.create(ruser=request.user, other=other, msg=msg or "", image=image, video=video)
            return redirect("message", ids)

    chats = Message.objects.filter(ruser=request.user, other=other) | Message.objects.filter(ruser=other, other=request.user)
    chats = chats.order_by("datetime")

    context = {
        'chats': chats,
        'other': other
    }
    return render(request, 'message.html', context)



def delete_message(request, ids):
    message = get_object_or_404(Message, id=ids)

    # Ensure only sender or receiver can delete
    if request.user == message.ruser or request.user == message.other:
        # Figure out who the "other" user is, so we can redirect to the conversation
        other_user = message.other if message.ruser == request.user else message.ruser
        message.delete()
        return redirect('message', ids=other_user.id)

    return redirect('message',ids=ids)  # or show 403 Forbidden page
