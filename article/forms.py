from django import forms
from .models import Article, Group, GroupMembers
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","article_image"]

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields ='__all__'

class AddMember(forms.ModelForm):
    class Meta:
        model = GroupMembers
        fields = ["group","members"]
