from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper


def index(request):
	return render(request, 'agency/index.html')


class NewspaperListView(generic.ListView):
	model = Newspaper
	paginate_by = 4
	template_name = 'agency/index.html'
