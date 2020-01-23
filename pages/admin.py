from django.db import models
from django.contrib import admin
from martor.widgets import AdminMartorWidget
from mptt.admin import MPTTModelAdmin

from .models import Page


class PageAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'markdown_content', 'created_at', 'is_published')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'meta_robots'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Page, PageAdmin)
