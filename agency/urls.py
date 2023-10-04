from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from agency.views import (
    NewspaperListView,
    NewspaperDetailView,
    TopicListView,
    RedactorListView,
    NewspaperCreateView,
    TopicNewsListView,
    RedactorNewsListView,
    NewspaperDeleteView,
    NewspaperUpdateView,
    register_request,
    RedactorUpdateView,
)

urlpatterns = [
    path("", NewspaperListView.as_view(), name="index"),
    path("newspaper/create", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspaper/<int:pk>", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/<int:pk>/update", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspaper/<int:pk>/delete", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register_request, name="register"),
    path("redactor/<int:redactor_id>", RedactorNewsListView.as_view(), name="redactor-news"),
    path("redactor/<int:pk>/update", RedactorUpdateView.as_view(), name="redactor-update"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topic/<str:topic_name>", TopicNewsListView.as_view(), name="topic-news"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "agency"
