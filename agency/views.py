from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperCreateForm, NewspaperSearchForm, TopicSearchForm, RedactorSearchForm
from agency.models import Newspaper, Topic, Redactor


def index(request):
    return render(request, 'agency/index.html')


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 4
    template_name = 'agency/index.html'
    queryset = Newspaper.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperCreateForm


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 4
    queryset = Topic.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(initial={"name": title})
        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


def topic_news_list(request, topic_name):
    queryset = Newspaper.objects.filter(topic__name=topic_name).order_by('-published_date')
    items_per_page = 4

    title = request.GET.get("title", "")
    search_form = NewspaperSearchForm(initial={"title": title})

    form = NewspaperSearchForm(request.GET)

    if form.is_valid():
        queryset = queryset.filter(
            title__icontains=form.cleaned_data["title"]
        )

    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'topic_name': topic_name,
        'newspaper_list': news,
        'page_obj': news,  # Pass the 'news' object as 'page_obj'
        'paginator': paginator,  # Pass the 'paginator' object
        "is_paginated": news.has_other_pages,
        "search_form": search_form
    }

    return render(request, 'agency/topic_news_list.html', context)


class RedactorListView(generic.ListView):
    model = Redactor
    queryset = Redactor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


def redactor_news_list(request, redactor_id):
    redactor = Redactor.objects.get(id=redactor_id)
    redactor_name = redactor.username
    queryset = Newspaper.objects.filter(publishers__id=redactor_id).order_by('-published_date')

    items_per_page = 4

    title = request.GET.get("title", "")
    search_form = NewspaperSearchForm(initial={"title": title})

    form = NewspaperSearchForm(request.GET)

    if form.is_valid():
        queryset = queryset.filter(
            title__icontains=form.cleaned_data["title"]
        )

    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'redactor_name': redactor_name,
        'newspaper_list': news,
        'page_obj': news,
        'paginator': paginator,
        "is_paginated": news.has_other_pages,
        "search_form": search_form
    }

    return render(request, 'agency/redactor_news_list.html', context)