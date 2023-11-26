from django.contrib import admin
from .models import NewsSource, NewsArticle, UserProfile, ArticleComment

# Register your models here
admin.site.register(NewsSource)
admin.site.register(NewsArticle)
admin.site.register(UserProfile)
admin.site.register(ArticleComment)
