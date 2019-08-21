from django.contrib import admin
from django.urls import path
from . import views
app_name = "article"

urlpatterns = [
    # path('dashboard/',views.dashboard,name = "dashboard"),
    path('create/',views.addArticle,name ="addarticle"),
    path('<int:id>',views.detail,name = "detail"),
    path('update/<int:id>',views.updateArticle,name = "update"),
    path('delete/<int:id>',views.deleteArticle,name = "delete"),
    path('', views.articles, name="articles"),
    path('group/create', views.createGroup, name="group"),
    path('comment/<int:id>', views.addComment, name="comment"),
    path('group/<int:id>/', views.groupdetails, name="gdetail"),
    path('connect/add/', views.add_friends, name="add_friends"),
    path('connect/remove/<int:pk>', views.groupdetails, name="remove_friends"),
]
