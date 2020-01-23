from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from markdown2 import markdown
from martor.models import MartorField
from mptt.models import MPTTModel, TreeForeignKey

from utils.models import MetaTagsMixin


class PageQuerySet(models.QuerySet):
    def published(self):
        return self.filter(Q(is_published=True))


class Page(MPTTModel, MetaTagsMixin):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children',
                            db_index=True,
                            on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),
                               editable=False,
                               verbose_name=_('Author'),
                               related_name='pages',  # user.entries.pages()
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             help_text=_('255 characters'),
                             verbose_name=_('Title'))
    slug = models.SlugField(help_text=_('Page slug'),
                            verbose_name=_('Slug'))
    path = models.TextField(unique=True, null=True, editable=False)  # full page path
    html_content = models.TextField(editable=False,
                                    blank=True)
    markdown_content = MartorField()
    created_at = models.DateTimeField(auto_now=False,
                                      auto_now_add=False,
                                      default=timezone.now,
                                      verbose_name=_('Publication date'))
    is_published = models.BooleanField(default=False,
                                       verbose_name=_('Published'))
    hits = models.IntegerField(default=0, editable=False)
    objects = PageQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = ('parent', 'slug',)
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page-details', args=[self.path])

    def add_hits(self):
        # Pages view counter
        if self.hits is not None:
            self.hits += 1
            self.save()
        else:
            self.hits = 0

    def get_path(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except self.DoesNotExist:
            ancestors = []
        else:
            ancestors = [item.slug for item in ancestors]
        return '/'.join(ancestors)

    def save(self, *args, **kwargs):
        super(Page, self).save()
        extras = {
            'fenced-code-blocks': None,
            'highlightjs-lang': None,
            'html-classes': {'img': 'img-fluid'},
            'spoiler': None,
            'strike': None,
            'tables': None,
        }
        self.html_content = markdown(self.markdown_content, extras=extras)
        self.path = self.get_path()
        super(Page, self).save()
