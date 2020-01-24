from django.db import models
from django.utils import timezone


class SoftDeletableQuerySet(models.QuerySet):
    """ A queryset that allows soft-delete on its objects """

    def delete(self, **kwargs):
        self.update(deleted_at=timezone.now(), **kwargs)

    def hard_delete(self, **kwargs):
        super(**kwargs).delete()
