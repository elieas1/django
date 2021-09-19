from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    followers = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": self.followers,
            "following": self.following,
        }

class Post(models.Model):
    name = models.TextField(null=False,default = "")
    posts = models.TextField(null=False,default = "")
    date = models.DateTimeField(default = datetime.now())
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.name} posted {self.posts}"

    def serialize(self):
        return {
            "name": self.name,
            "post": self.posts,
            "date":self.date,
            "likes":self.likes
        }

class Following(models.Model):
    followinguser = models.TextField(null=False,default = "")
    followeduser = models.TextField(null=False,default = "")
    
    def __str__(self):
        return f"{self.followinguser} follows {self.followeduser}"

    def serialize(self):
        return {
            "followinguser": self.followinguser,
            "followeduser": self.followeduser,
        }

class Likes(models.Model):
    user = models.TextField(null=False,default = "")
    like = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likedpost")
    
    def __str__(self):
        return f"{self.user} liked {self.like}"

    def serialize(self):
        return {
            "user": self.user,
            "like": self.like,
        }