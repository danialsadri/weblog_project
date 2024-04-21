from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    classes = ('collapse',)
    show_change_link = True


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    classes = ('collapse',)
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'publish', 'reading_time', 'status', 'category']
    list_filter = ['status', ('publish', JDateFieldListFilter)]
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    list_display_links = ['author', 'title']
    list_editable = ['status', 'category']
    ordering = ['title', 'publish']
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'subject']
    list_filter = ['subject']
    search_fields = ['name', 'description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = [("created", JDateFieldListFilter), ("updated", JDateFieldListFilter)]
    search_fields = ['name', 'description']
    list_editable = ['active']
    raw_id_fields = ['post']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']
    list_filter = [('created', JDateFieldListFilter)]
    search_fields = ['title', 'description']
    raw_id_fields = ['post']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'job']
    list_filter = [('date_of_birth', JDateFieldListFilter)]
    search_fields = ['user']
    raw_id_fields = ['user']
