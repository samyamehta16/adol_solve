from django.urls import path
from . import views
from .views import PostListView,PostCreateView,PostDetailView,add_comment_to_post
urlpatterns = [
    path('',views.home,name="Home"),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('adol_solve/',views.solve_prob,name='solve_problem'),
    path('post_list', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('tasks/', views.task_list, name='task_list'),
    path('complete_task/', views.complete_task, name='complete_task'),
    path('contact/',views.contact,name='Contact')
    #path('search/', views.search_posts, name='search_posts'),
]