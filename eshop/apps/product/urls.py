from django.urls import re_path
from django.conf import settings
from .views import *

# urls
categories_url = r"^" + settings.API_URL + r"categories/?$"
categories_url_pk = r"^" + settings.API_URL + r"categories/(?P<pk>\d+)/?$"
category_url = r"^" + settings.API_URL + r"category/?$"
category_url_pk = r"^" + settings.API_URL + r"category/(?P<pk>\d+)/?$"

products_url = r"^" + settings.API_URL + r"products/?$"
producs_url_pk = r"^" + settings.API_URL + r"products/(?P<pk>\d+)/?$"
product_url = r"^" + settings.API_URL + r"product/?$"
produc_url_pk = r"^" + settings.API_URL + r"product/(?P<pk>\d+)/?$"

urlpatterns = [
    re_path(categories_url, CategoryListAllApi().as_view(), name="categories"),
    re_path(categories_url_pk, CategoryListAllApi().as_view(), name="categories"),
    re_path(category_url, CategoryCreateApi().as_view(), name="category"),
    re_path(category_url_pk, CategoryRetrieveUpdateDestroyApi().as_view(), name="category"),
    
    re_path(products_url, ProductListAllApi().as_view(), name="products"),
    re_path(producs_url_pk, ProductListAllApi().as_view(), name="products"),
    re_path(product_url, ProductCreateApi().as_view(), name="product"),
    re_path(produc_url_pk, ProductRetrieveUpdateDestroyApi().as_view(), name="product"),
]
