from django.urls import re_path
from .views import *

# urls
categories_url = r"^categories/?$"
categories_url_pk = r"^categories/(?P<pk>\d+)/?$"
category_url = r"^category/?$"
category_url_pk = r"^category/(?P<pk>\d+)/?$"

products_url = r"^products/?$"
producs_url_pk = r"^products/(?P<pk>\d+)/?$"
product_url = r"^product/?$"
produc_url_pk = r"^product/(?P<pk>\d+)/?$"

urlpatterns = [
    re_path(categories_url, CategoryListAllApi().as_view(), name="categories"),
    re_path(categories_url_pk, CategoryListAllApi().as_view(), name="categories-pk"),
    re_path(category_url, CategoryCreateApi().as_view(), name="category"),
    re_path(category_url_pk, CategoryRetrieveUpdateDestroyApi().as_view(), name="category-pk"),
    
    re_path(products_url, ProductListAllApi().as_view(), name="products"),
    re_path(producs_url_pk, ProductListAllApi().as_view(), name="products-pk"),
    re_path(product_url, ProductCreateApi().as_view(), name="product"),
    re_path(produc_url_pk, ProductRetrieveUpdateDestroyApi().as_view(), name="product-pk"),
]
