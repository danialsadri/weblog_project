from modeltranslation.translator import TranslationOptions, register
from .models import *


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ['title', 'description']


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ['name', 'description']


@register(Account)
class AccountTranslationOptions(TranslationOptions):
    fields = ['bio', 'job']
