import datetime
import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from markdown2 import markdown
from martor.models import MartorField
from mptt.models import MPTTModel, TreeForeignKey


def get_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    path = 'uploads' + datetime.datetime.today().strftime('/%Y/%m/%d/')
    os.makedirs(path, mode=0o755, exist_ok=True)
    return os.path.join(path, filename)


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(Q(is_published=True))


class Post(models.Model):
    CONTENT_SEPARATOR = '<!--MORE-->'
    category = TreeForeignKey('Category',
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),
                               editable=False,
                               verbose_name=_('Author'),
                               related_name='all',  # user.entries.all()
                               on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_upload_path,
                              blank=True,
                              help_text=_('Post image'),
                              verbose_name=_('Post image'))
    title = models.CharField(max_length=255,
                             help_text=_('255 characters'),
                             verbose_name=_('Title'))
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text=_('Post slug, unique for post date'),
                            verbose_name=_('Slug'))
    html_excerpt = models.TextField(editable=False,
                                    blank=True)
    html_content = models.TextField(editable=False,
                                    blank=True)
    markdown_content = MartorField()
    tags = models.ManyToManyField('Tag',
                                  verbose_name=_('Tags'),
                                  blank=True,
                                  related_name='all')  # tag.entries.all()
    pub_date = models.DateTimeField(auto_now=False,
                                    auto_now_add=False,
                                    default=timezone.now,
                                    verbose_name=_('Publication date'))
    is_published = models.BooleanField(default=False,
                                       verbose_name=_('Published'))
    hits = models.IntegerField(default=0, editable=False)
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-details', args=[
            int(self.pub_date.year), int(self.pub_date.month),
            int(self.pub_date.day), str(self.slug)
        ])

    def add_hits(self):
        # Posts view counter
        if self.hits is not None:
            self.hits += 1
            self.save()
        else:
            self.hits = 0

    def save(self, *args, **kwargs):
        extras = {
            'fenced-code-blocks': None,
            'highlightjs-lang': None,
            'html-classes': {'img': 'img-fluid'},
            'spoiler': None,
            'strike': None,
            'tables': None,
        }
        if self.CONTENT_SEPARATOR in self.markdown_content:
            excerpt, content = self.markdown_content.split(
                self.CONTENT_SEPARATOR, 1)
            self.html_excerpt = markdown(excerpt, extras=extras)
            self.html_content = markdown(content, extras=extras)
        else:
            self.html_excerpt = ''
            self.html_content = markdown(self.markdown_content, extras=extras)

        super(Post, self).save()


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children',
                            db_index=True,
                            on_delete=models.CASCADE)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug',)
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def save(self, *args, **kwargs):
        slug_list = self.get_slug_list(self)

        super(Category, self).save()

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(max_length=255,
                             help_text=_('255 symbols max'),
                             verbose_name=_('Tag name'))
    slug = models.SlugField(unique=True,
                            verbose_name=_('Slug'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title
