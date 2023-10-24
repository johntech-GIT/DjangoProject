# 1
#User.objects.create_user('FirstdUser')
#User.objects.create_user('SecondUser')

# 2

#us1=User.objects.get(pk=1)
#Author.objects.create(user =us1)
#us2=User.objects.get(pk=2)
#Author.objects.create(user =us2)

# 3

#Category.objects.create(name='Наука')
#Category.objects.create(name='Политика')
#Category.objects.create(name='Спорт')
#Category.objects.create(name='IT-технологии')
#Category.objects.create(name='Здравоохранение')

#4

# post1=Post(title = 'Все горячие клавиши Windows 10.', author = Author.objects.get(id = 1) )
# post1.save()
# P1= Post.objects.all()[0]
# P1.content= 'Во многих случаях лучше всего обратиться к горячим клавишам, вместо' \
#             ' того, чтобы делать вручную рутинные действия, скопировать, вставить,вырезать.'
# P1.save()


# post2=Post(title = 'Александра Трусова — жизнь на льду и отношения с Тутберидзе и Плющенко', author = Author.objects.get(id = 1) )
# P2= Post.objects.all()[1]
# P2.content='Александра Трусова – талантливая, харизматичная, красивая и феноменальная юная российская фигуристка.'\
# ' Родилась Александра в городе Рязань'\
# 'в многодетной семье.Среди троих детей у родителей Саша являлась старшим ребёнком.'\
# ' Отец и мать всегда придерживались здорового образа жизни, такое же отношение воспитывали и в детях.'
# P2.save()

# post3=Post(choi_public = 'New', title = 'ВОЗ признала вред прививок от коронавируса после окончания пандемии.', author = Author.objects.get(id = 2) )
# P3.content='Всемирная организация здравоохранения изменила рекомендации по вакцинации от ковида. Долгое время качество вакцин и побочные явления от пр
# ививок были табу.'
# P3.save()

# 5

# cat2 = Category.objects.get(name='Спорт')
# p2 = Post.objects.get(title='Александра Трусова — жизнь на льду и отношения с Тутберидзе и Плющенко')
# pc1=PostCategory(cat=cat2, post=p2)
# pc1.save()

# Ct=Category.objects.all()
# p1 = Post.objects.get(title='Все горячие клавиши Windows 10.')
# p3 = Post.objects.get(title='ВОЗ признала вред прививок от коронавируса после окончания пандемии.')
# PostCategory(post = p1, cat = Ct[3]).save()
# PostCategory(post = p3, cat = Ct[0]).save()
# PostCategory(post = p3, cat = Ct[4]).save()

# 6

# uscom=User.objects.all()
# postcom=Post.objects.all()
# Comment(post = postcom[0], user = uscom[0], content = 'спасибо за труд. отличный гайд').save()
# Comment(post = postcom[0], user = uscom[1], content = 'А что означает сочетание клавиш "Crtl+Alt+1" ?').save()
# Comment(post = postcom[1], user = uscom[0], content = 'Зачем у шестнадцатилетний девушки в биографии писать
# -не замужем, разве может быть по другому').save()
# Comment(post = postcom[1], user = uscom[1], content = 'Как можно говорить, что родилась в многодетной семье,
# если Саша - первый ребенок???? Ну и вот это С поездок. Русский язык лучше подучить, прежде чем рваться на Дзен
# деньги зарабатывать.').save()
# Comment(post = postcom[2], user = uscom[1], content = 'Это они что? Отморозились типа? Сами советы давали,
# а теперь напопятую?').save()

# 7

#p = Post.objects.get(id = 2)
#p.like()
#p.like()
#p.like()
#p.like()
#p.like()
#p = Post.objects.get(id = 3)
#p.like()
#p.like()
#p.like()
#p.dislike()
#p.dislike()
#p.like()
#p.like()
#p.like()
#p = Post.objects.get(id = 4)
#p.dislike()
#p.dislike()
#p.like()
#p.dislike()

#C = Comment.objects.all()
# C[0].like()
# C[0].dislike()
# C[0].like()
# C[0].like()
# C[0].like()
# C[0].like()
# C[1].like()
# C[1].like()
# C[1].like()
# C[1].like()
# C[2].like()
# C[2].like()
# C[2].like()
# C[3].like()
# C[3].like()
# C[3].like()
# C[3].like()
# C[3].like()
# C[4].like()
# C[4].like()
# C[4].like()
# C[4].like()
# C[4].like()
# C[4].like()
# C[4].like()

# 8

# a = Author.objects.all()[0]
# a.update_rating()
# a = Author.objects.all()[1]
# a.update_rating()

# 9

# bu = Author.objects.all().order_by('-rating').values('user','rating')[0]
# User.objects.filter(id = bu['user']).values('username')[0]['username']
# bu['rating']

# 10

# bp = Post.objects.all().order_by('-_rating')[0]
# print(f"Создано - {bp.time_create}\nИмя автора - {bp.author.user.username}\nрейтинг - {bp._rating}\nТайтл - {bp.title}\nПревью - {Post.preview(bp)}")

# 11

# com = Comment.objects.filter(post = bp)
# for _ in range(len(com)):
#   us = ""
#   us += 'Создано - ' + str(com[_].time_create) + "\n"
#   us += 'Пользователь - ' + str(com[_].user) + "\n"
#   us += 'Рейтинг - ' + str(com[_].rating) + "\n"
#   us += 'Содержание - ' + str(com[_].content) + "\n"
#   print(us)

# pip install django
# pip install django-allauth
# pip install django-filter==21.1
# pip install django-apscheduler


# python manage.py shell
# from NewsPortal.models import *
# exit()

#  test2user@mail.com     rtrytfjygkghkukbkkb  'hkvoviwxgujovrsc'
#  test3user@mail.com     ododdodhjkij444
# teaexpansion78@gmail.com  treveler78
