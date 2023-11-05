from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class NewsSource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(null=True)  # URL to the small image for the article
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_articles = models.ManyToManyField(NewsArticle, related_name='saved_by', blank=True)

    def __str__(self):
        return self.user.username

class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"

class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    # hello = models.CharField(max_length=1, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
