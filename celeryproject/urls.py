from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from celeryweb import views

urlpatterns = [url(r'^news/$', views.news, name='news'),
               url(r'^news/(?P<slug>[\w-]*)', views.news, name='news_entry'),
               url(r'^tutorials/$', views.tutorials, name='tutorials'),
               url(r'^tutorials/(?P<slug>[\w-]*)',
                   views.tutorials, name='tutorial'),
               url(r'^community/$', views.community,
                   name='external_resources'),
               url(r'^profile/(?P<username>.+)/',
                   views.user_profile, name='user_profile'),

               # AJAX
               url(r'^ajax/stackoverflowquestions/(?P<page_size>[0-9]+)/(?P<page>[0-9]+)/$',
                   'stackoverflow_questions',
                   name='stackoverflow_questions'),
               url(r'^ajax/packageinfo/$',
                   views.package_info,
                   name='package_info'),

               # ADMIN
               url(r'^admin/', include(admin.site.urls)),
               url(r'^$', views.home, name='home'),
               ] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True
        },),
    ]
