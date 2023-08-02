from django.db import models
from django.contrib.auth.models import User
from django.db.models import *
from django.core.validators import MinValueValidator
from django.urls import reverse

# (password = '!ma1xFZ92ONPsUtHVjClyRbwA8doW4hJx2lUxgcTw':'F1_user_enter', username = 'FirstUser', last_name = 'First', email = 'First@mail.com', first_name = 'F_User')
# (password = '!KnLLujclySzijT7D9fuen1wy8UvLfmRKrrKypJUX', username = 'SecondUser', last_name = 'Second', email = 'Second@mail.com', second_name = 'S_User')
# ThirdUser:'T3_user_enter'
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # id пользователя (кто создатель)
    rating = models.IntegerField(default=0)  # рейтинг создателя

    def update_rating(self):
        Pr = Post.objects.filter(author=self).aggregate(Sum('_rating'))['_rating__sum'] * 3
        Cr = Comment.objects.filter(user=self.user).aggregate(Sum('_rating'))['_rating__sum']

        def upcr(auth=self):
            UPCr_sum = 0
            for Qp in Post.objects.filter(author=auth).values('id'):
                UPCr_sum += Comment.objects.filter(post=Post.objects.get(pk=Qp['id'])).aggregate(Sum('_rating'))[
                    '_rating__sum']
            return UPCr_sum

        UPCr = upcr()
        self.rating = UPCr + Pr + Cr
        self.save()
        return self.rating

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)  # название категории
    subscribers = models.ManyToManyField(User, related_name="categories") # поле subscribers имеет связь ManyToMany
    # к модели юзер через алиас categories пример: user.categories.all()

    def __str__(self):
        return self.name.title()


class PostCategory(models.Model):
    post = models.ForeignKey('Post', null=True, on_delete=models.SET_NULL)  # id статьи/новости
    cat = models.ForeignKey(Category, on_delete=models.PROTECT)  # id категории


class Post(models.Model):
    POSITIONS = [
        ('New', 'Новость'),
        ('Art', 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # id создателя статьи/новости
    choi_public = models.CharField(max_length=3,
                                   choices=POSITIONS,
                                   default='Art')
    time_create = models.DateTimeField(auto_now_add=True)  # дата и время создания статьи/новости
    cat = models.ManyToManyField(Category, through=PostCategory)  # id категории статьи/новости
    title = models.CharField(max_length=255)  # заголовок статьи/новости
    content = models.TextField(blank=True)  # содержание статьи/новости
    _rating = models.IntegerField(default=0, db_column='rating')  # рейтинг статьи/новости


    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def preview(self):
        return str(self.content)[:124] + '...'

    def __str__(self):
        return self.title#, self.content

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # id что комментировал
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # id кто комментировал
    content = models.TextField(blank=True)  # содержание комментария
    time_create = models.DateTimeField(auto_now_add=True)  # дата и время создания комментария
    _rating = models.IntegerField(default=0, db_column='rating')  # рейтинг комментария

    @property
    def rating(self):
        return self._rating

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

# from NewsPortal.models import *
