from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import DateDetailView

from .models import Post, Category


class PostListView(generic.ListView):
    queryset = Post.objects.published()
    allow_future = False
    paginate_by = 5


class PostDateDetailView(DateDetailView):
    queryset = Post.objects.published()
    date_field = 'pub_date'
    allow_future = False
    month_format = '%m'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.object.add_hits()
        return self.render_to_response(context)


def view_posts_by_category(request, slug=None):
    category_slug_list = slug.split('/')

    try:
        post = Category.objects.get(slug=category_slug_list[-1])
    except:
        post = get_object_or_404(Post, slug=category_slug_list[-1])
        return render(request, "blog/post_detail.html", {'post': post})
    else:
        return render(request, 'blog/category.html', {'post': post})