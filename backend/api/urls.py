from django.urls import path
from .views import (
    api_root,
    profile_picture,
    profile_cv,
    contact_view,
    hire_view,
    ProjectListCreateView,
    sync_github_projects
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('profile/picture/', profile_picture, name='profile-picture'),
    path('profile/cv/', profile_cv, name='profile-cv'),
    path('contact/', contact_view, name='contact'),
    path('hire/', hire_view, name='hire'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/sync-github/', sync_github_projects, name='sync-github'),
]
