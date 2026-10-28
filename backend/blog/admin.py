from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tag', 'created_at')
    list_filter = ('tag',)
    search_fields = ('title', 'body')
