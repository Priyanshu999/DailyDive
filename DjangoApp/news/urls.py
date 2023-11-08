from django.urls import path
from news import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),

]