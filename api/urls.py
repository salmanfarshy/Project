from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, ProjectListCreateView, ProjectDetailView, TaskDetailView, TaskListCreateView, CommentListCreateView, CommentDetailView

urlpatterns = [
    # user route
    path('users/register/', RegisterView.as_view(), name='user_register'),
    path('users/login/', LoginView.as_view(), name='user_login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # project route
    path('projects/', ProjectListCreateView.as_view(), name='projects-view-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-details'),
    # task route
    path('projects/<int:project_id>/tasks/', TaskListCreateView.as_view(), name='task-view-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-details'),
    # comment route
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='comment-view-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-details'),
]
