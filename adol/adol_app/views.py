from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django import template
from django.db.models import Q
from .forms import UserRegistrationForm,CommentForm,PostForm
from .models import Post,Comment,Task,UserProfile
from django.views.generic import ListView,DetailView,CreateView
def home(request):
    return render(request,"adol_app/home.html")
#register_user
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
#login_user
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('Home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
register = template.Library()
#log_user out
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')
#nav bar link to solve_prob
def solve_prob(request):
    return render(request,"adol_app/solve_prob.html")

class PostListView(ListView):
    model = Post
    template_name = 'adol_app/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'adol_app/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'adol_app/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'adol_app/add_comment_to_post.html', {'form': form})
@login_required
def task_list(request):
    tasks = Task.objects.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    completed_tasks = user_profile.completed_tasks.all()
    remaining_tasks = tasks.exclude(id__in=completed_tasks.values_list('id', flat=True))
    progress = (completed_tasks.count() / tasks.count()) * 100 if tasks.count() > 0 else 0

    return render(request, 'adol_app/task_list.html', {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'remaining_tasks': remaining_tasks,
        'progress': progress,
    })

@login_required
def complete_task(request):
    if request.method == 'POST':
        selected_tasks = request.POST.getlist('task')

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        for task_name in selected_tasks:
            task = Task.objects.get(title=task_name)
            user_profile.completed_tasks.add(task)

    return redirect('task_list')
def contact(request):
    return render(request,"adol_app/contact.html")