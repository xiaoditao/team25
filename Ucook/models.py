from django.db import models
from django.contrib.auth.models import User
# from Ucook.models import Comment

class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default= None,on_delete=models.PROTECT)
    time = models.DateTimeField()
    username = models.CharField(max_length=200)

    def _str_(self):
        return 'Post by '+self.user+'text=" ' +self.text+'"'


class Profile(models.Model):

    user = models.ForeignKey(User, default= None,on_delete=models.PROTECT)
    bio_text = models.CharField(max_length=200,editable= True)
    profile_picture = models.FileField(blank=False)
    content_type = models.CharField(max_length=50)
    # followers = models.ManyToManyField(User, related_name='follows', symmetrical=False)


    def _str_(self):
        return 'id= '+self.id+'text=" ' +self.bio+'"'

class Comment(models.Model):
    text = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    post = models.ForeignKey(Post,on_delete=models.PROTECT)
    time = models.DateTimeField()
    def _str_(self):
        return 'id =  '+ self.id +'text=" ' + self.text + '"'