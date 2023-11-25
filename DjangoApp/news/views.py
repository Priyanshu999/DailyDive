from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.edit import FormView
from .forms import CustomSignupForm, NewCommentForm, UserProfileForm
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.db.models import Count
from django.contrib.auth import login
from django.db.models.functions import TruncDate
from .models import NewsArticle, ArticleComment, NewsSource, UserProfile
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from verify_email.email_handler import send_verification_email
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib.auth.models import User

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm
    success_url = '/'  # Provide the URL name for the 'home' view

    def form_valid(self, form):
        send_verification_email(self.request, form)
        user = form.instance
        # user = form.save()
        login(self.request, user)  # Log the user in
        return super().form_valid(form)
    

class HomeView(ListView):
    model = NewsArticle
    template_name = 'index.html'
    # context_object_name = 'articles'
    paginate_by = 14

    def get_queryset(self):
        # Create an initial queryset for articles
        articles = NewsArticle.objects.all()

        # Apply additional filtering based on your requirements
        articles = self.mix_articles(articles)

        # Slice the filtered queryset
        articles = articles.order_by('-publication_date')[:300]

        return articles


    def mix_articles(self, articles):
        # Group articles by the date part of publication_date and annotate the count
        articles = articles.annotate(
            publication_date_date=TruncDate('publication_date')
        ).values('publication_date_date').annotate(
            article_count=Count('id')
        )

        # Sort the grouped articles by count in descending order
        articles = articles.order_by('-article_count')

        # Extract the date parts from the grouped result
        publication_date_dates = articles.values_list('publication_date_date', flat=True)

        # Fetch and order the articles based on the sorted date parts
        sorted_articles = NewsArticle.objects.filter(publication_date__date__in=publication_date_dates).order_by('-publication_date')
        return sorted_articles
    


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the original article object
        article = context['article']

        # Split the article content into paragraphs
        paragraphs = article.content.split('.')

        # Separate the first paragraph
        first_paragraph = paragraphs[0]
        
        # Split the remaining content into two halves
        remaining_content = paragraphs[1:]
        half_length = len(remaining_content) // 2
        first_half = remaining_content[:half_length]
        second_half = remaining_content[half_length:]
        first_half_content = ".".join(first_half) + "."
        second_half_content = ".".join(second_half) + "."
        
        comments_connected = ArticleComment.objects.filter(
            article=self.get_object()).order_by('-timestamp')

        # Create a custom context dictionary
        custom_context = {
            'article': article,
            'first_paragraph': first_paragraph,
            'first_half_content': first_half_content,
            'second_half_content': second_half_content,
        }

        custom_context['comments'] = comments_connected
        if self.request.user.is_authenticated:
            custom_context['comment_form'] = NewCommentForm(instance=self.request.user)

        context.update(custom_context)
        return context
    

    def post(self, request, *args, **kwargs):
        new_comment = ArticleComment(content=request.POST.get('content'),
                                  user=self.request.user,
                                  article=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
    

class SourceNewsView(ListView):
    model = NewsArticle
    template_name = 'source_news.html'
    paginate_by = 20
    substrings_to_remove = ["%2520", "%20"]

    def get_queryset(self):
        source_name = self.kwargs['source_name']
        print(source_name)
        source_name = self.remove_substrings(source_name, self.substrings_to_remove)
        # Get the source based on the name
        source = NewsSource.objects.get(name=source_name)
        # Get articles from the specific source
        articles = NewsArticle.objects.filter(source=source)
        return articles
    
    def remove_substrings(self, main_string, substrings_to_remove):
        for substring in substrings_to_remove:
            main_string = main_string.replace(substring, ' ')
        return main_string
    

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('user_profile')  # Adjust 'profile' to the name of your user profile URL

    def get_object(self, queryset=None):
        # Get the UserProfile instance for the current user
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TnCview(TemplateView):
    template_name = 'tnc.html'


class ToggleBookmarkView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        article = get_object_or_404(NewsArticle, pk=pk)
        user_profile, create = UserProfile.objects.get_or_create(user=request.user)
        print("Hello")
        print(user_profile.saved_articles.all())

        if article in user_profile.saved_articles.all():
            print("removing")
            user_profile.saved_articles.remove(article)
            print(len(user_profile.saved_articles.all()))
            print(user_profile.saved_articles.all())

        else:
            user_profile.saved_articles.add(article)
            print("adding")
            print(len(user_profile.saved_articles.all()))
            print(user_profile.saved_articles.all())

        # Redirect back to the news detail page
        return HttpResponseRedirect(reverse('news_detail', args=[pk]))
    

class BookMarkView(LoginRequiredMixin, ListView):
    model = NewsArticle
    template_name = 'bookmarks.html'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.usert.saved_articles.all()


@login_required
def upvote_comment(request, comment_id):
    comment = ArticleComment.objects.get(pk=comment_id)

    # Check if the user has already upvoted
    print("Hello {} upvoted".format(request.user))
    if request.user not in comment.upvotes.all():
        comment.upvotes.add(request.user)
        comment.downvotes.remove(request.user)

    return JsonResponse({'upvotes': comment.number_of_likes})


@login_required
def downvote_comment(request, comment_id):
    comment = ArticleComment.objects.get(pk=comment_id)

    # Check if the user has already downvoted
    if request.user not in comment.downvotes.all():
        comment.downvotes.add(request.user)
        comment.upvotes.remove(request.user)

    return JsonResponse({'downvotes': comment.number_of_likes})


