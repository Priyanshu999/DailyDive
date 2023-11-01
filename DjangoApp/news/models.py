from django.db import models
from django.contrib.auth.models import User

class NewsSource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    
    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_sources = models.ManyToManyField(NewsSource, related_name='favorited_by', blank=True)
    saved_articles = models.ManyToManyField(NewsArticle, related_name='saved_by', blank=True)
    
    def __str__(self):
        return self.user.username

class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"

class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
