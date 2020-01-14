from django.db import models


class MPTT(models.Model):
    title = models.CharField(verbose_name='Title',
                             max_length=255)
    left = models.IntegerField(blank=True,
                               null=True)
    right = models.IntegerField(blank=True,
                                null=True)
    parent = models.ForeignKey(verbose_name='Parental category',
                               to='self',
                               blank=True,
                               null=True,
                               related_name='children',
                               on_delete=models.CASCADE)
    position = models.IntegerField(verbose_name='Position',
                                   blank=True,
                                   null=True)
    level = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(verbose_name='Published at', default=True)

    def __unicode__(self):
        level = self.level if self.level else 1
        i = u'| ' if level > 1 else ''
        return (u'|--' * (level - 1)) + i + self.title

    class Meta:
        ordering = ('left',)

    def save(self, *args, **kwargs):
        super(MPTT, self).save(*args, **kwargs)
        self.build_mptt_tree()

    def build_mptt_tree(self, left=1, parent=None, level=1):
        for i in type(self).objects.filter(parent=parent).order_by('position'):
            obj, children_count = i, 0
            while obj.children.exists():
                for child in obj.children.all():
                    children_count += 1
                    obj = child
            data = {
                'level': level,
                'left': left,
                'right': left + (children_count * 2) + 1
            }
            type(self).objects.filter(id=i.id).update(**data)
            left = data['right'] + 1
            self.build_mptt_tree(left=data['left'] + 1,
                                 parent=i.id,
                                 level=data['level'] + 1)
