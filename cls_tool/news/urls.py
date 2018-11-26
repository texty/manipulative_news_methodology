from django.urls import path
from . import views

urlpatterns = [
    path(r'done/', views.edit, name='list_done'),
    path(r'edit/<int:pk>/', views.edit_done, name='edit_done'),
    path(r'ajax/feedback/', views.feedback, name='feedback'),
    path(r'', views.classify, name='classify'),
]