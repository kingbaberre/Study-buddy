from django.db import models
from django.contrib.auth.models import User
from quiz.models import Category
# from ckeditor.fields import models.TextField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name = "Author")
    title = models.CharField(max_length=50, verbose_name="Title")
    topic = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Creation Date")
    article_image = models.FileField(blank = True,null = True,verbose_name="Add Photo to Article")
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']
class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete = models.CASCADE,verbose_name = "article",related_name="comments")
    comment_author = models.CharField(max_length = 50,verbose_name = "Name")
    comment_content = models.CharField(max_length = 200,verbose_name = "Comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']

class Group(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Group Name",unique=True)
    user = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name="owner")
    
    def __str__(self):
        return self.name

class GroupMembers(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,verbose_name="my group")
    members = models.ManyToManyField(User)

    @classmethod
    def make_friend(cls, new_friend):
        friend, created = cls.objects.get_or_create(
        )
        friend.users.add(new_friend)
    
    @classmethod
    def lose_friend(cls, new_friend):
        friend, created = cls.objects.get_or_create(
    
        )
        friend.users.remove(new_friend)
