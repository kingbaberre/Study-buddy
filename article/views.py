from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm, GroupForm
from .models import Article, Comment, Group
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles": articles})
    articles = Article.objects.all()

    return render(request, "discussion/index.html", {"articles": articles})


def index(request):
    return render(request, "index.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)

        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")
    return render(request, "discussion/addarticle.html", {"form": form})


def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request, "discussion/detail.html", {"article": article, "comments": comments})


@login_required(login_url="user:login")
def updateArticle(request, id):

    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None,
                       request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)

        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla güncellendi")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form})


@login_required
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)

    article.delete()

    messages.success(request, "Makale Başarıyla Silindi")

    return redirect("article:dashboard")


@login_required
def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author,
                             comment_content=comment_content)

        newComment.article = article

        newComment.save()
    return redirect(reverse("article:detail", kwargs={"id": id}))


@login_required
def createGroup(request):
    mygroups = Group.objects.all()
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('article:articles')
    return render(request, 'discussion/creategroup.html', {"form": form, "mygroups": mygroups})


@login_required
def groupdetails(request, id):
    group = get_object_or_404(Group, id=id)
    suggested = User.objects.all()
    return render(request, 'discussion/group-details.html', {"group": group, "suggested": suggested})


def add_friends(request, pk):
    friend = User.objects.get(pk=pk)
    GroupMembers.make_friend(request.user, friend)
    return redirect('article:articles')


def remove_friends(request, pk):
    friend = User.objects.get(pk=pk)
    GroupMembers.lose_friend(request.user, friend)
    return redirect('article:articles')
