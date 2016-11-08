from django.conf.urls import patterns, include, url
from django.contrib import admin
#from controlcenter.views import controlcenter

admin.autodiscover()

urlpatterns = patterns('pushell.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^api/user/$', 'api_user'),
    url(r'^skin_config/$', 'skin_config', name='skin_config'),
    url(r'^login/$', 'Login', name='login'),
    url(r'^logout/$', 'Logout', name='logout'),
    url(r'^exec_cmd/$', 'exec_cmd', name='exec_cmd'),
    url(r'^file/upload/$', 'upload', name='file_upload'),
    url(r'^file/download/$', 'download', name='file_download'),
    url(r'^setting', 'setting', name='setting'),
    url(r'^terminal/$', 'web_terminal', name='terminal'),
    url(r'^juser/', include('juser.urls')),
    url(r'^jasset/', include('jasset.urls')),
    url(r'^jlog/', include('jlog.urls')),
    url(r'^jperm/', include('jperm.urls')),
    #url(r'^admin/', admin.site.urls),
    #url(r'^admin/dashboard/', controlcenter.urls),
#urlpatterns = patterns('',
    #url(r'^$', 'dj2auth.views.Signin', name='home'),
    #url(r'^gauth/$', 'dj2auth.views.GAuth',name='home'),
    #url(r'^demo/', include('demo.foo.urls')),
    #url(r'^admin/', include(admin.site.urls)),
 )
