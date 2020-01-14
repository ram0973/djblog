from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('<path:path>/', views.PageDetailView.as_view(
        date_field='created_at'),
        name='page-details'),
]
