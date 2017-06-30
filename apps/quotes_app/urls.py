from django.conf.urls import url
from . import views
app_name= 'quotes'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^add_to_faves$', views.add_to_faves, name='add_to_faves'),
    url(r'^add_a_quote$', views.add_a_quote, name='add_a_quote'),
    url(r'^remove_fave$', views.remove_fave, name='remove_fave'),
    url(r'^user/(?P<id>\d+)$', views.user_page, name='user_page'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^home$', views.home, name='home'),
]
