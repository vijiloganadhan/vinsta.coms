from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('signup/',views.signup_views,name="signup"),
    path('login/',views.login_views,name="login"),
    path('logout/',views.logout_views,name="logout"),
    path('',views.homes,name="home"),
    path('createprofile',views.createuserprofile,name="createprofile"),
    path('editprofile/<int:ids>',views.edit_user_profile,name="editprofile"),
    path('create_post',views.post_create,name="create"),
    path('postview/<int:ids>',views.post_view,name="postuser"),
    path('delete_post/<int:ids>',views.post_delete,name="deletepost"),
    path('uploadreels',views.reels_upload,name='uploadreels'),
    path('watchreels',views.watch_reels,name="reels"),
    path("comments/<int:ids>",views.comments_user,name="comments"),
    path("search_post",views.post_search,name="search_post"),
    path('search_profile',views.search,name="search_profile"),
    path("userprofile/<int:ids>",views.user_profile,name="userprofiledetails"),
    path('profileview/<int:ids>/',views.target_profile,name="profileview"),
    path('follow/<int:ids>',views.follow,name="follow"),
    path('unfollow/<int:ids>',views.unfollow,name="unfollow"),
    path("messages/<int:ids>",views.message_with_others,name="message"),
    path("delete_msg/<int:ids>",views.delete_message,name="msg_delete"),
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

