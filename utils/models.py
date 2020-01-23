from django.db import models
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


def get_meta_item(name, content):
    return loader.render_to_string('utils/meta.html', {'name': name, 'content': content}) if name and content \
        else ''


class MetaTagsMixin(models.Model):
    """ Abstract base class for html meta tags """

    class Meta:
        abstract = True

    meta_title = models.CharField(
        _('Title'),
        max_length=255,
        blank=True,
        help_text=_('Seo page title'))
    meta_description = models.CharField(
        _('Description'),
        max_length=255,
        blank=True,
        help_text=_('Seo page description'))
    meta_keywords = models.CharField(
        _('Keywords'),
        max_length=255,
        blank=True,
        help_text=_('Seo keywords, separate keywords with comma'))
    meta_robots = models.CharField(
        _('Robots'),
        max_length=255,
        blank=True,
        help_text=_('Seo robots, separate keywords with comma'))

    def get_meta_title(self):
        return get_meta_item('title', self.meta_title)

    def get_meta_description(self):
        return get_meta_item('description', self.meta_description)

    def get_meta_keywords(self):
        return get_meta_item('keywords', self.meta_keywords)

    def get_meta_robots(self):
        return get_meta_item('robots', self.meta_robots)

    def get_meta_tags(self):
        return mark_safe('\n'.join((
            self.get_meta_title(),
            self.get_meta_description(),
            self.get_meta_keywords(),
            self.get_meta_robots(),
        )))
