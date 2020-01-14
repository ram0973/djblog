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

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Page, PageAdmin)
