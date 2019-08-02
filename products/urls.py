from django.conf.urls import url
from . import views

app_name = 'products'

urlpatterns = [
    url(r'^$', views.Product_list, name='all'),
    url(r'^new/$', views.sell_product, name='create'),
    url(r'^detail/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='detail'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeleteProduct.as_view(), name='delete'),
    url(r'^search/$', views.search_product, name='search'),

]
