from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from jdatetime import datetime
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES = (
        ('برنامه-نویسی-وب', 'برنامه نویسی وب'),
        ('طراحی-وبسایت', 'طراحی وبسایت'),
        ('برنامه-نویسی-موبایل', 'برنامه نویسی موبایل'),
        ('هوش-مصنوعی', 'هوش مصنوعی'),
        ('سایر', 'سایر'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name=_('نویسنده'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    description = models.TextField(max_length=500, verbose_name=_('توضیحات'))
    slug = models.SlugField(max_length=200, verbose_name=_('اسلاگ'))
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name=_('تاریخ انتشار'))
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))
    reading_time = models.PositiveIntegerField(verbose_name=_('زمان مطالعه'))
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name=_('وضعیت'))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='سایر', verbose_name=_('دسته بندی'))

    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='blog:post_detail', kwargs={'post_id': self.id})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            storage, path = image.image_file.storage, image.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    description = models.TextField(max_length=500, verbose_name=_('توضیحات'))
    email = models.EmailField(max_length=100, verbose_name=_('ایمیل'))
    phone_number = models.CharField(max_length=11, verbose_name=_('شماره تلفن'))
    subject = models.CharField(max_length=100, verbose_name=_('موضوع'))

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت ها')

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('پست'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    description = models.TextField(max_length=500, verbose_name=_('توضیحات'))
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name=_('تاریخ ویرایش'))
    active = models.BooleanField(default=False, verbose_name=_('وضعیت'))

    objects = jmodels.jManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنت ها')

    def __str__(self):
        return self.name


def get_image_post(instance, filename):
    return f"post_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name=_('پست'))
    image_file = ResizedImageField(upload_to=get_image_post, size=[500, 300], crop=['middle', 'center'],
                                   quality=100, verbose_name=_('تصویر'))
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('عنوان'))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('توضیحات'))
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))

    objects = jmodels.jManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = _('تصویر')
        verbose_name_plural = _('تصویر ها')

    def __str__(self):
        return self.title if self.title else self.image_file.name

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)


def get_image_account(instance, filename):
    return f"account_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', verbose_name=_('کاربر'))
    date_of_birth = jmodels.jDateTimeField(blank=True, null=True, verbose_name=_('تاریخ تولد'))
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('بایوگرافی'))
    job = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('شغل'))
    photo = ResizedImageField(upload_to=get_image_account, size=[500, 300], crop=['middle', 'center'],
                              quality=100, verbose_name=_('تصویر'))

    objects = jmodels.jManager()

    class Meta:
        verbose_name = _('اکانت')
        verbose_name_plural = _('اکانت ها')

    def __str__(self):
        return self.user.username
