from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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
	fields = ['title', 'content', 'topic', 'publishers']
	success_url = reverse_lazy('agency:index')


class TopicListView(generic.ListView):
	model = Topic
	paginate_by = 4


class RedactorListView(generic.ListView):
	model = Redactor
