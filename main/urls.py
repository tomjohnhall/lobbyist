from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^postcode/', views.postcode, name='postcode'),
    url(r'^clearPostcode/', views.clearPostcode, name='clearPostcode'),
    url(r'^petitions/', views.petitions, name='petitions'),
]
