from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^userdetails/(\d+)/(\w+)/$', views.profile, name='profile'),
    # url(r'^new/question/$', views.new_question, name='new_question'),
    url(r'^edit/profile/$', views.edit_profile, name='edit_profile'),
    # url(r'^rate/post/(\d+)$', views.rate_website, name='rate_website'),
    url(r'about/$', views.MoriSpaceView.as_view()),
    url(r'test_partial/$', views.UpdateItemsView.as_view()),
]

# this will help to serve uploaded images on the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
