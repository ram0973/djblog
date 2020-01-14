from django.db import models
from django.contrib import admin
from martor.widgets import AdminMartorWidget
from .models import Post, Category, Tag
from mptt.admin import MPTTModelAdmin


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Tag)
