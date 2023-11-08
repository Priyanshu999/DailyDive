from django.views.generic.edit import FormView
from .forms import CustomSignupForm
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import F, Subquery, Window, Count, Max
from django.contrib.auth import login
from django.db.models.functions import Rank, DenseRank, TruncDate
from .models import NewsArticle
# from verify_email.email_handler import send_verification_email
# from django.shortcuts import render, re
# from django.views import View
# from django.contrib.auth.models import User

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm
    success_url = '/'  # Provide the URL name for the 'home' view

    def form_valid(self, form):
        # send_verification_email(self.request, form)
        # user = form.instance
        user = form.save()
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

        # Create a custom context dictionary
        custom_context = {
            'article': article,
            'first_paragraph': first_paragraph,
            'first_half_content': first_half_content,
            'second_half_content': second_half_content,
        }

        context.update(custom_context)
        return context