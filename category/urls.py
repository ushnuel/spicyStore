from django.conf.urls import url
from . import views

app_name = 'categories'

urlpatterns = [
    url(r'^$', views.CategoryList.as_view(), name='all'),
    url(r'^new/$', views.CreateCategory.as_view(), name='create'),
    url(r'^products/in/(?P<slug>[-\w]+)/$', views.CategoryDetail.as_view(), name='detail'),

]
