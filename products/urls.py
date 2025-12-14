from django.urls import path
from . import views
from . import api_views

app_name = "products"

urlpatterns = [
    path(
        "",
        views.ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "category/<slug:category_slug>/",
        views.ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        "<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),

    # API endpoints (from earlier)
    path("api/products/", api_views.ProductListAPI.as_view(), name="product_list_api"),
    path("api/products/<slug:slug>/", api_views.ProductDetailAPI.as_view(), name="product_detail_api"),
]
"""urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
#API
    path("api/products/", api_views.ProductListAPI.as_view(), name="product_list_api"),
    path("api/products/<slug:slug>/", api_views.ProductDetailAPI.as_view(), name="product_detail_api"),
]"""