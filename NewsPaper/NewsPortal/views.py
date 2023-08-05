from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.db import transaction
from .forms import CreatePost, UserUpdateForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404, render, reverse



class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'News.html'
    context_object_name = 'Post'
    paginate_by = 5


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'NewsDet.html'
    context_object_name = 'new1'


class FilterNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'Post'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin,CreateView):
    form_class = CreatePost
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        if self.request.path == '/News/news/create/':
            Post.choi_public = 'New'
        Post.save()
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin,UpdateView):
    form_class = CreatePost
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = CreatePost
    model = Post
    template_name = 'post_create.html'


class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    form_class = CreatePost
    model = Post
    template_name = 'post_edit.html'


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('news_list')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.request.user.username}'
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'profile_update.html'
    #success_url = reverse_lazy('profile_detail')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_update')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(cat=self.category,).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subskriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context