from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/list/', views.post_list, name='post_list'),
    path('post/list/<str:category>/', views.post_list, name='post_list_category'),
    path('post/detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
    path('ticket/', views.ticket, name='ticket'),
    path('profile/', views.profile, name='profile'),
    path('profile/post/create/', views.post_create, name='post_create'),
    path('profile/post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('profile/post/update/<int:post_id>/', views.post_update, name='post_update'),
    path('profile/image/delete/<int:image_id>/', views.image_delete, name='image_delete'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/account/', views.edit_account, name='edit_account'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
