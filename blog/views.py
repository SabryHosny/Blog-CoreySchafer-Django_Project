from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import (Post)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)

# Create your views here.


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/HOME.html", context)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'  # default => post_list
    template_name = "blog/HOME.html"  # defualt => blog/post_list.html
    # by default that is the template name it looks for => <app>/<model>_<viewtype>.html
    # views.PostListView.as_view(template_name='blog/HOME.html') => you can do this into urls as well
    # order posts from newest( to be at the top) to oldest( to be at the bottom)
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/user_posts.html"
    paginate_by = 5

    # override this method to modify the queryset that the ListView returns
    # kwargs: the query parameters(parameters sent through the url)
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # template_name defualt = "post_form.html"
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# NOTE : UpdateView is very similar to CreateView
# UserPassesTestMixin =>use that to make sure that the user who make the post is only one who able to update it
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # template_name defualt = "post_form.html"
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # a function defined into UserPassesTestMixin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        # you can also say => return self.request.user == post.author :)


# NOTE: DeleteView is very similar to DetailView
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # template_name => default: post_confirm_delete.html
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/ABOUT.html", {"title": "About"})
