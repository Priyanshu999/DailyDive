from django.contrib import admin
from .models import NewsSource, NewsArticle, UserProfile, ArticleLike, ArticleComment

# Register your models here
admin.site.register(NewsSource)
admin.site.register(NewsArticle)
admin.site.register(UserProfile)
admin.site.register(ArticleLike)
admin.site.register(ArticleComment)
