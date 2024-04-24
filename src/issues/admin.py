from django.contrib import admin

from .models import Issue


@admin.register(Issue)
class Issueadmin(admin.ModelAdmin):
    list_display = ["id", "title", "junior", "senior"]
