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
    article_link = models.URLField(default="")
    image_url = models.URLField(null=True)  # URL to the small image for the article
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    publication_date = models.DateTimeField()

    @property
    def number_of_comments(self):
        return ArticleComment.objects.filter(article=self).count()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="usert", on_delete=models.CASCADE)
    saved_articles = models.ManyToManyField(NewsArticle, related_name='saved_by', null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class ArticleComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    upvotes = models.ManyToManyField(User, related_name='comment_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='comment_downvotes', blank=True)

    @property
    def number_of_likes(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        if self.article:
            return f"Comment by {self.user.username} on {self.article.title}"
        else:
            return "A comment"


