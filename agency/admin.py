from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from agency.models import Redactor, Newspaper, Topic


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = ('username', 'years_of_experience')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Personal info",
            {'fields': ("first_name", "last_name", 'years_of_experience', "profile_image")}
        ),
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Other", {"fields": ("profile_image",)}),
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('title', "topic", "published_date")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
