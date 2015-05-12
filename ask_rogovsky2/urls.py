from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'ask_rogovsky2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^helloworld/', 'ask_rogovsky2.views.helloworld', name='helloworld'),
    url(r'^login/$', 'ask_rogovsky2.views.login', name='login'),
    url(r'^logout/$', 'ask_rogovsky2.views.logout_view', name='logout'),
    url(r'^(\w*)$', 'ask_rogovsky2.views.questions', name='questions'),
    url(r'^signup/$', 'ask_rogovsky2.views.signup', name='signup'),
    url(r'^question/(\d+)$', 'ask_rogovsky2.views.question', name='question'),
    url(r'^ask/$','ask_rogovsky2.views.ask', name='ask'),
    url(r'^tag/(.+)$', 'ask_rogovsky2.views.bytag', name='tag'),
    url(r'^profile/edit/$', 'ask_rogovsky2.views.profile_edit', name='p_edit'),
    url(r'^rate/$', 'ask_rogovsky2.views.rate', name='rate'),
    url(r'^right/$', 'ask_rogovsky2.views.right', name='right')
]
