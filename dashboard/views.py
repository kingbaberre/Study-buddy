from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from quiz.models import Category
from .forms import SignUpForm,UserUpdateForm,ProfileUpdateForm
from django.views.generic import ListView,DetailView
from django.db.models import Q  # new


# Create your views here.
@login_required
def index(request):
    category = Category.objects.order_by('name')
    users = User.objects.all()
    # thread = Thread.objects.all()
    my_dic ={'category':category,'users':users}
    return render(request,'registration/home.html',context=my_dic)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def landing(request):
    return render(request,'index.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)


class SearchResultsView(ListView):
    model = User
    template_name = 'discussion/search.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('search')
        object_list = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        )
        return object_list

def myprofile(request,id):
    myprofile = User.objects.get(pk=id)
    return render(request,'registration/user-details.html',{'myprofile':myprofile})