from django.contrib import admin
from .models import Post,Profile,Reels,Comments,Follow_user,Message

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Reels)
admin.site.register(Comments)
admin.site.register(Follow_user)
admin.site.register(Message)
