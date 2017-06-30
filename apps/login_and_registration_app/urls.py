from django.conf.urls import url
from . import views
app_name = 'auth'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^validate_registration$', views.validate_registration, name='register'),
    url(r'^validate_login$', views.validate_login, name='login'),
    url(r'^success$', views.success, name='success'),
]
