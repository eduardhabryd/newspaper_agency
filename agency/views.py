from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperCreateForm
from agency.models import Newspaper, Topic, Redactor


def index(request):
    return render(request, 'agency/index.html')


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 4
    template_name = 'agency/index.html'


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperCreateForm


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 4


def topic_news_list(request, topic_name):
    news_list = Newspaper.objects.filter(topic__name=topic_name).order_by('-published_date')
    items_per_page = 4

    paginator = Paginator(news_list, items_per_page)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'topic_name': topic_name,
        'news': news,
        'page_obj': news,  # Pass the 'news' object as 'page_obj'
        'paginator': paginator,  # Pass the 'paginator' object
        "is_paginated": news.has_other_pages
    }

    return render(request, 'agency/topic_news_list.html', context)


class RedactorListView(generic.ListView):
    model = Redactor


def redactor_news_list(request, redactor_id):
    redactor = Redactor.objects.get(id=redactor_id)
    redactor_name = redactor.username
    news_list = Newspaper.objects.filter(publishers__id=redactor_id).order_by('-published_date')

    items_per_page = 4

    paginator = Paginator(news_list, items_per_page)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'redactor_name': redactor_name,
        'news': news,
        'page_obj': news,  # Pass the 'news' object as 'page_obj'
        'paginator': paginator,  # Pass the 'paginator' object
        "is_paginated": news.has_other_pages
    }

    return render(request, 'agency/redactor_news_list.html', context)