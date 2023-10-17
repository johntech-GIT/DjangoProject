from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.db import transaction
from .forms import CreatePost, UserUpdateForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User#, Group
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
Password = os.getenv("Password")
Mail = os.getenv("Mail")


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


class ProfileUpdate_View(LoginRequiredMixin, UpdateView):
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
        return super(ProfileUpdate_View, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_update')

class CategoryListView(ListView):  # вьюха для просмотра всех постов выбраной категории
    model = Post # на основе модели Post
    template_name = 'category_list.html' # указываем шаблон
    context_object_name = 'category_news_list' # обзываем контекст
    ordering = '-time_create'
    paginate_by = 10

    def get_queryset(self): # функция переопределения кверисета
        self.category = get_object_or_404(Category, id=self.kwargs['pk']) # получаем выбранную категорию
        queryset = Post.objects.filter(cat=self.category,).order_by('-time_create') # получаем все посты выбранной категории
        # упорядочиваем по дате создания и записываем в переменную queryset
        return queryset # возвращаем queryset

    def get_context_data(self, **kwargs): #
        context = super().get_context_data(**kwargs) #
        context['is_not_subsсriber'] = self.request.user not in self.category.subscribers.all() #
        context['category'] = self.category #
        return context #

@login_required
def subscribe(request, pk): # функция подписки на категорию
    user = request.user # получаем юзера с которым ведем сессию
    category = Category.objects.get(id=pk)  # получаем id выбранной категории
    useremail = user.email
    message = 'Вы успешно подписались на рассылку новостей категории'  # создаем сообщение
    usersubs = category.subscribers.filter(id=user.id)#.exsists():
    #usersubs = usersubs[id]

    #if not category.subscribers.filter(id=user.id).exsists():

    category.subscribers.add(user) # в промежуточной таблице (category.subscribers) создаем строку category_id user_id
    html = render_to_string(
        'mail/subscribed.html',
        {'category': category,
            'user': user,
        }
    )

    msg = EmailMultiAlternatives(
    subject=f'{category} subscription',
    body='',
    from_email=Mail,
    to=[useremail,],
    )
    msg.attach_alternative(html, 'text/html')

    try:
        msg.send()
    except Exception as e:
        print(e)
    #return redirect('news_list')
    print(useremail)
    print(Mail)
    print(Password)
    #return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'subscribe.html', {'category': category, 'message': message}) # выводим соообщение



#41:30

@login_required
def unsubscribe(request, pk): # функция отписки на категорию
    user = request.user # получаем юзера с которым ведем сессию
    category = Category.objects.get(id=pk) # получаем id категории
    category.subscribers.remove(user) # из промежуточной таблицы (category.subscribers) удаляем строку category_id user_id

    message = 'Вы успешно отписались от рассылки новостей категории' # создаем сообщение
    return render(request, 'unsubscribe.html', {'category': category, 'message': message}) # выводим соообщение