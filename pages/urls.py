from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('pages/<slug:slug>/', views.ViewPage, name='page'),
]
