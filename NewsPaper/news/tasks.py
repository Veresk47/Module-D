from celery import shared_task
import time
from .models import Post, Category
from django.template.loader import render_to_string
from NewsPaper import settings
from django.core.mail import EmailMultiAlternatives
import datetime

@shared_task
def hello():
    time.sleep(10)
    print('hello world')

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task()
def info_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscribers_emails = []

    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)

    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}{pk}'

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,

    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task()
def one_week_notice():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject= 'Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()