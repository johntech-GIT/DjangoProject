from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from NewsPaper import PassW


def get_subscriber(category): # функция для создания списка имейлов пользователей подписанных на конкретную категорию
    user_email = [] # создаем пустой список
    for user in category.subscribers.all(): # в модели category итерируемся по связи subscribers с моделью user
        user_email.append(user.email)  # плюсуем имеил юзера к списку
    return user_email # возвращаем полученный список


def new_post_subscription(instance): # функция для отправки почтового сообщения принимает экземпляр класса post
    template = 'mail/new_post.html'  # указываем шаблон

    for category in instance.category.all(): # итерируемся по всем категориям в instance (экземпляре класса post)
        email_subject = f'New post in category: "{category}"'  # тема сообщения для рассылки
        user_emails = get_subscriber(category) # вызываем get_subscriber() для сбора имейлов подписчиков

    html = render_to_string(   # создаем содержимое сообщения вызывая render_to_string()
        template_name=template, # вписываем шаблон
        context={               # вписываем содержимое
            'category': category, # категорию
            'post' : instance,    # и саму публикацию
        }
    )
    msg = EmailMultiAlternatives(  # создаем полное сообщение, куда вписываем:
        subject=email_subject, # тему
        body='',  # само сообщение
        from_email=PassW[0],  # с какого адреса рассылка
        to=user_emails  # на какие адреса разослать (список)
    )

    msg.attach_alternative(html, 'text/html')  # указываем в каком виде разослать
    msg.send()  # рассылаем