from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', _('پیشنهاد')),
        ('انتقاد', _('انتقاد')),
        ('گزارش', _('گزارش')),
    )
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('نام'))
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
                                  label=_('توضیحات'))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}), label=_('ایمیل'))
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   label=_('شماره تلفن'))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}),
                                label=_('موضوع'))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if not phone_number.isnumeric():
                raise forms.ValidationError(_('شماره تلفن عددی نیست'))
            else:
                return phone_number


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            if len(name) > 100:
                raise forms.ValidationError('نام بیشتر از 100 کاراکتر نباید باشد')
            else:
                return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            if len(description) > 500:
                raise forms.ValidationError('نام بیشتر از 500 کاراکتر نباید باشد')
            else:
                return description


class SearchForm(forms.Form):
    query = forms.CharField()


class PostCreateForm(forms.ModelForm):
    image1 = forms.ImageField(label=_('تصویر اول'), widget=forms.FileInput(attrs={'class': 'form-control'}))
    image2 = forms.ImageField(label=_('تصویر دوم'), widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': "con-name"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'reading_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class PostUpdateForm(forms.ModelForm):
    image1 = forms.ImageField(label=_('تصویر اول'), widget=forms.FileInput(attrs={'class': 'form-control'}))
    image2 = forms.ImageField(label=_('تصویر دوم'), widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': "con-name"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'reading_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label=_('پسورد'))
    password2 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label=_('تکرار پسورد'))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('پسورد ها باید مطابقت داشته باشند')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label=_('نام کاربری'))
    password = forms.CharField(max_length=200, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_('پسورد'))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'job', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
