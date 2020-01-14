from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views import generic
from django.views.generic import DateDetailView
from .models import Post, Category


class PostListView(generic.ListView):
    queryset = Post.objects.published()
    allow_future = False
    paginate_by = 5


class PostDateDetailView(DateDetailView):
    queryset = Post.objects.published()
    date_field = 'created_at'
    allow_future = False
    month_format = '%m'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        self.object.add_hits()
        return self.render_to_response(context)


def view_posts_by_category(request, path):
    category = get_object_or_404(Category, path=path)
    posts = get_list_or_404(Post, category=category)
    return render(request, 'blog/category.html', {'post_list': posts, 'path': path, 'category': category})
