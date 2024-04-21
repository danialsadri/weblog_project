from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = []
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('rosetta/', include('rosetta.urls')),
)
admin.sites.AdminSite.site_title = _('پنل مدیریت')
admin.sites.AdminSite.site_header = _('پنل مدیریت')
admin.sites.AdminSite.index_title = _('پنل مدیریت')
