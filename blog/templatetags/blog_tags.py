from django import template
from django.db.models import Count, Max, Min
from blog.models import *
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.simple_tag()
def most_active_users(count=5):
    return User.objects.annotate(users_count=Count('user_posts')).order_by('-users_count')[:count]


@register.simple_tag()
def most_study_time():
    return Post.published.aggregate(Max('reading_time'))


@register.simple_tag()
def minimum_study_time():
    return Post.published.aggregate(Min('reading_time'))


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=5):
    l_posts = Post.published.order_by('-publish')[:count]
    return {'l_posts': l_posts}


@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter()
def replace_names_with_asterisk(value):
    names = ['جک', 'جان']
    for name in names:
        value = value.replace(name, '***')
    return value
