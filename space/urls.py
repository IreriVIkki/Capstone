from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


urlpatterns = [
    # authentication urls
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    # pages urls
    url(r'morispace/$', views.MoriSpaceView.as_view(), name='home'),
    url(r'^userdetails/(\d+)/(\w+)/$', views.profile, name='profile'),
    url(r'^edit/profile/$', views.edit_profile, name='edit_profile'),
    url(r'new_item/$', views.UpdateItemsView.as_view(), name='new_item'),
]

# this will help to serve uploaded images on the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
