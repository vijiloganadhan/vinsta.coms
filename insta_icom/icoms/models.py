from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, FileField
from django.contrib.auth.models import User  # still can reference Django user
from datetime import datetime

  # replace with your actual database name


# Post Model
class Post(Document):
    CHOICES = [
        ('image', 'image'),
        ('video', 'video'),
    ]
    title = StringField(max_length=100, required=True)
    desc = StringField()
    type = StringField(choices=CHOICES)
    image = FileField()
    video = FileField()
    user = ReferenceField(User)
    meta = {'collection': 'post'}


# Profile Model
class Profile(Document):
    user = ReferenceField(User)
    name = StringField(max_length=100)
    desc = StringField()
    image = FileField()
    following_count = IntField(default=0)
    followers_count = IntField(default=0)

    def __str__(self):
        return str(self.user) if self.user else "No User"

    meta = {'collection': 'profile'}


# Reels Model
class Reels(Document):
    image = FileField()
    captions = StringField(max_length=100)
    date = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User)
    video = FileField()

    def __str__(self):
        return f'{self.captions} - {self.date}'

    meta = {'collection': 'reels'}


# Comments Model
class Comments(Document):
    comments_user = ReferenceField(User, required=False)
    reply_comments = ReferenceField(User, required=False)
    message = StringField()
    post = ReferenceField(Post)
    datetime = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.comments_user.username}-{self.message}" if self.comments_user else self.message

    meta = {'collection': 'comments'}


# Follow_user Model
class Follow_user(Document):
    following = ReferenceField(User, required=False)
    followers = ReferenceField(User, required=False)
    datetime = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.followers.username} followed by {self.following.username}"

    meta = {'collection': 'follow_user'}


# Message Model
class Message(Document):
    ruser = ReferenceField(User, required=False)
    other = ReferenceField(User, required=False)
    image = FileField()
    video = FileField()
    datetime = DateTimeField(default=datetime.utcnow)
    msg = StringField()

    def __str__(self):
        return f"req_user - {self.ruser.username} - other - {self.other.username}"

    meta = {'collection': 'message'}
