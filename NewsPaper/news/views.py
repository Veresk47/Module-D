from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.views import View
from .models import Author, Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .tasks import hello, printer
from datetime import datetime, timedelta


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/author.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'news/post_detail.html'

class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    context_object_name = 'news'
    template_name = 'news/Post_list.html'
    paginate_by = 5


class PostSearch(ListView):
    model = Post
    ordering = 'dateCreation'
    context_object_name = 'news'
    template_name = 'news/Post_list_search.html'
    paginate_by = 2


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewsCreate( CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)



class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'



class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')



class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})

class IndexView(View):
    def get(self, request):
        printer.apply_async([10], eta = datetime.now() + timedelta(seconds=5))
        hello.delay()
        return HttpResponse('Hello')