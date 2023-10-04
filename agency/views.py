from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (
	NewspaperCreateForm,
	NewspaperSearchForm,
	TopicSearchForm,
	RedactorSearchForm,
	RedactorCreationForm,
	RedactorUpdateForm
)

from agency.models import Newspaper, Topic, Redactor


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

	def form_valid(self, form):
		newspaper = form.save(commit=False)
		if 'image' in self.request.FILES:
			newspaper.image = self.request.FILES['image']
		newspaper.save()
		form.save_m2m()
		return super().form_valid(form)


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = Newspaper
	success_url = reverse_lazy('agency:index')
	form_class = NewspaperCreateForm

	def form_valid(self, form):
		newspaper = form.save(commit=False)
		if 'image' in self.request.FILES:
			newspaper.image = self.request.FILES['image']
		newspaper.save()
		form.save_m2m()
		return super().form_valid(form)


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
	model = Newspaper
	success_url = reverse_lazy('agency:index')


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


class TopicNewsListView(generic.ListView):
	model = Newspaper
	template_name = 'agency/topic_news_list.html'
	context_object_name = 'newspaper_list'
	paginate_by = 4

	def get_queryset(self):
		topic_name = self.kwargs['topic_name']
		queryset = super().get_queryset()
		title = self.request.GET.get("title", "")

		if title:
			queryset = queryset.filter(title__icontains=title)

		return queryset.filter(topic__name=topic_name).order_by('-published_date')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['topic_name'] = self.kwargs['topic_name']
		context['search_form'] = NewspaperSearchForm(initial={"title": self.request.GET.get("title", "")})
		return context


class RedactorListView(generic.ListView):
	model = Redactor
	queryset = Redactor.objects.all()

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(RedactorListView, self).get_context_data(**kwargs)
		full_name = self.request.GET.get("full_name", "")
		context["search_form"] = RedactorSearchForm(initial={"full_name": full_name})
		return context

	def get_queryset(self):
		form = RedactorSearchForm(self.request.GET)

		if form.is_valid():
			full_name = form.cleaned_data["full_name"].split()
			first_name = None
			last_name = None
			any_name = None

			if len(full_name) > 1:
				first_name = full_name[0]
				last_name = full_name[1]
			else:
				any_name = form.cleaned_data["full_name"]

			if first_name:
				self.queryset = self.queryset.filter(
					first_name__icontains=first_name
				)

			if last_name:
				self.queryset = self.queryset.filter(
					last_name__icontains=last_name
				)

			if any_name:
				self.queryset = self.queryset.filter(
					Q(first_name__icontains=any_name)
					| Q(last_name__icontains=any_name)
				)

		return self.queryset


class RedactorUpdateView(generic.UpdateView):
	model = Redactor
	success_url = reverse_lazy('agency:index')
	template_name = 'agency/redactor_update.html'
	form_class = RedactorUpdateForm

	def get_form(self, form_class=None):
		# Pass the request user to the form
		form = super().get_form(form_class)
		form.user = self.request.user
		return form

	def form_valid(self, form):
		redactor = form.save(commit=False)
		if 'profile_image' in self.request.FILES:
			redactor.profile_image = self.request.FILES['profile_image']
		redactor.save()
		form.save_m2m()

		# Handle password change
		password_form = PasswordChangeForm(self.request.user, self.request.POST)
		if password_form.is_valid():
			password_form.save()
			# Update the session to prevent logout after password change
			update_session_auth_hash(self.request, password_form.user)

		return super().form_valid(form)


class RedactorNewsListView(generic.ListView):
	model = Newspaper
	template_name = 'agency/redactor_news_list.html'
	context_object_name = "newspaper_list"
	paginate_by = 4

	def get_queryset(self):
		redactor_id = self.kwargs['redactor_id']
		title = self.request.GET.get("title", "")
		queryset = super().get_queryset()

		if title:
			queryset = queryset.filter(title__icontains=title)

		return queryset.filter(publishers__id=redactor_id).order_by('-published_date')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		redactor = Redactor.objects.get(id=self.kwargs["redactor_id"])
		context["redactor_name"] = redactor.get_full_name()
		context["search_form"] = NewspaperSearchForm(initial={"title": self.request.GET.get("title", "")})
		return context


def register_request(request):
	if request.method == "POST":
		form = RedactorCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect("agency:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RedactorCreationForm()
	return render(request=request, template_name="registration/register.html", context={"form": form})
