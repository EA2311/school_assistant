from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import index
from school_assistant import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('accounts.urls')),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),
    path('', index, name='index'),

    path('api/', include('api.urls')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
