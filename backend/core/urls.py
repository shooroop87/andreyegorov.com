from django.urls import path
from .views import index, about, projects, blog, contacts

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('blog/', blog, name='blog'),
    path('contacts/', contacts, name='contacts'),
]