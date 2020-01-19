from django.db import models
from django.utils.translation import gettext as _


class SEO(models.Model):
    class Meta:
        abstract = True
    seo_desc = models.TextField(
        verbose_name=_("SEO Meta description"),
        blank=True,
        max_length=500)
    seo_title = models.CharField(
        verbose_name=_("SEO Title override"),
        blank=True,
        max_length=120)
    seo_noindex = models.BooleanField(
        verbose_name=_("SEO Block indexing by search engine robots"),
        default=False)
