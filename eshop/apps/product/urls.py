from django.urls import re_path
from django.conf import settings
from .views import *

urlpatterns = [
    re_path(
        r"^" + settings.API_URL + r"categories/?$",
        CategoryListAllApi().as_view(),
        name="categories",
    ),
    re_path(
        r"^" + settings.API_URL + r"category/?$",
        CategoryDetailApi().as_view(),
        name="category",
    ),
    re_path(
        r"^" + settings.API_URL + r"products/?$",
        ProductListAllApi().as_view(),
        name="products",
    ),
    re_path(
        r"^" + settings.API_URL + r"product/?$",
        ProdcutsDetailApi().as_view(),
        name="product",
    ),
]