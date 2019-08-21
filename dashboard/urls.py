from django.urls import path
from . import views
urlpatterns = [
    path('home',views.index,name="index"),
    path('',views.landing,name="landing"),
    path('register',views.register,name="register"),
    path('logout',views.logout,name="logout"),
    path('profile/edit', views.profile, name="profile"),
    path('profile/<int:id>/', views.myprofile, name="myprofile"),
    path('search', views.SearchResultsView.as_view(),name="search")
]
