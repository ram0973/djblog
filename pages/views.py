from django.views.generic import DetailView

from .models import Page


class PageDetailView(DetailView):
    queryset = Page.objects.published()
    date_field = 'created_at'
    allow_future = False
    slug_field = 'path'
    slug_url_kwarg = 'path'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.object.add_hits()
        return self.render_to_response(context)


class HomePageDetailView(DetailView):
    queryset = Page.objects.published()
    date_field = 'created_at'
    allow_future = False
    slug_field = 'path'
    slug_url_kwarg = 'path'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.object.add_hits()
        return self.render_to_response(context)
