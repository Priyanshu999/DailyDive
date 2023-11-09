from django.urls import path
from news import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('source/<str:source_name>/', views.SourceNewsView.as_view(), name='source_news'),
]