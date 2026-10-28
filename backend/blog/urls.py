from django.urls import path
from .views import BlogListCreateView, MyBlogsView, BlogDetailView

urlpatterns = [
    path('', BlogListCreateView.as_view()),
    path('mine/', MyBlogsView.as_view()),
    path('<uuid:pk>/', BlogDetailView.as_view()),
]
