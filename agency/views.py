from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper, Topic


def index(request):
	return render(request, 'agency/index.html')


class NewspaperListView(generic.ListView):
	model = Newspaper
	paginate_by = 4
	template_name = 'agency/index.html'


class NewspaperDetailView(generic.DetailView):
	model = Newspaper
	

class TopicListView(generic.ListView):
	model = Topic
	paginate_by = 4
