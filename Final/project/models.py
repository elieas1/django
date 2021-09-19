from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from slugify import slugify

# Create your models here.


class Page(models.Model):
    pagename = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.pagename

    def get_absolute_url(self):
        return reverse("page", kwargs={"page": self.pagename})


class User(AbstractUser):
    description = models.TextField(null=True, blank=True)
    pagesfollowed = models.ManyToManyField(Page, related_name="Userpages",blank=True)
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="Userfollowing")
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="Userfollowers")
    age = models.IntegerField(null=True, blank=True)
    upvotedposts = models.ManyToManyField('Post', related_name='postupvotes',symmetrical=False,blank=True)
    image = models.ImageField(upload_to='pictures', default='/pictures/default.jpg', null=True, blank=True)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"account": self.username})

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            "username": self.username,
            "following": [user.username for user in self.following.all()],
            "followers": [user.username for user in self.followers.all()],
            "followercount": self.followers.count(),
            "followingcount": self.following.count(),
            "count": [user.followers.count() for user in self.followers.all()],
            "upvotedposts":[post.title for post in self.upvotedposts.all()]

        }


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userpost")
    title = models.CharField(max_length=200)
    body = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="pagecategory")
    likes = models.IntegerField(null=True, default=0)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return (f'{self.username}:{self.title}')

    def get_absolute_url(self):
        slug = slugify(self.title)
        return reverse("post", kwargs={"postslug": slug})

    def serialize(self):
        return {
            "title": self.title,
            "body": self.body,
            "date": self.date,
            "likes": self.likes
        }


class Comment(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usercomment")
    comm = models.TextField(null=False)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="postcomment")
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return (f'{self.username} : {self.post}')

    def serialize(self):
        return {
            'user': {'username': self.username.username, 'image': self.username.image.url},
            "comment": self.comm,
            "upvotes": self.upvotes,
            "date": self.date,
            "upvotes": self.upvotes,
            "post": self.post.title
        }


class Email(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="emailsender")
    recipient = models.ManyToManyField(
        User, blank=True, related_name="emailrecipient")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} sent a mail to {[user.username for user in self.recipient.all()]}'

    def serialize(self):
        return {
            'sender': self.sender.username,
            'subject': self.subject,
            'body': self.body,
            'timestamp': self.timestamp.strftime("%d %b %H:%M %p"),
            'read': self.read,
            'archived': self.archived,
            'recipient': [user.username for user in self.recipient.all()]


        }
