from django.urls import path
from news import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('source/<str:source_name>/', views.SourceNewsView.as_view(), name='source_news'),
    path('news/upvote/<int:comment_id>/', views.upvote_comment, name='upvote_comment'),
    path('news/downvote/<int:comment_id>/', views.downvote_comment, name='downvote_comment'),
    path('news/<int:pk>/bookmark/', views.ToggleBookmarkView.as_view(), name='toggle_bookmark'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('signup/tnc/', views.TnCview.as_view(), name='tnc'),
]