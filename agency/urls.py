"""
URL configuration for newspaper_agency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from agency.views import (
    NewspaperListView,
    NewspaperDetailView,
    TopicListView,
    RedactorListView,
    NewspaperCreateView,
    topic_news_list,
    redactor_news_list,
    NewspaperDeleteView,
    NewspaperUpdateView,
    register_request
)

urlpatterns = [
    path("", NewspaperListView.as_view(), name="index"),
    path("newspaper/<int:pk>", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("newspaper/create", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("topic/<str:topic_name>", topic_news_list, name="topic-news"),
    path("redactor/<int:redactor_id>", redactor_news_list, name="redactor-news"),
    path("newspaper/<int:pk>/update", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspaper/<int:pk>/delete", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path("register/", register_request, name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "agency"
