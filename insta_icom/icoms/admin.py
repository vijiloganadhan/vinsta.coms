# from django.contrib import admin
from django_mongoengine import mongo_admin
from .models import Post,Profile,Reels,Comments,Follow_user,Message
mongo_admin.site.register(Post)
mongo_admin.site.register(Reels)
mongo_admin.site.register(Comments)
mongo_admin.site.register(Follow_user)
mongo_admin.site.register(Message)



# Register your models here.
# admin.site.register(Post)
# admin.site.register(Profile)
# admin.site.register(Reels)
# admin.site.register(Comments)
# admin.site.register(Follow_user)
# admin.site.register(Message)
