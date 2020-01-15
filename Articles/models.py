from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    created_at=models.DateField(auto_now_add=True) # the time never changes
    updated_at=models.DateField(auto_now=True)  #changes the time on insert
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='articles')

    def __str__(self):
        return self.title


class ArticleTest(models.Model):    #test table for articles , nullable foreign key
    title=models.CharField(max_length=50)
    content=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title
