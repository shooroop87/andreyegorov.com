from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.article_detail, name='article_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('privacy/', views.privacy, name='privacy'),
]