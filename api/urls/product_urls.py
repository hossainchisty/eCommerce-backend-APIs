from django.urls import path
from api.views import product_views as views

urlpatterns = [
    # Product management routers
    path("", views.getProductList.as_view(), name="products"),
    path("create", views.CreateProduct.as_view(), name="product-create"),
    path("update/<int:pk>", views.UpdateProduct.as_view(), name="product-update"),
    path("delete/<int:pk>", views.DeleteProduct.as_view(), name="product-delete"),
    path("<int:pk>/reviews/", views.createProductReview, name="review-create"),
    path("get/<int:pk>", views.getProduct, name="getProduct"),
    path("top", views.getTopProduct, name="TopratedProduct"),
    path("similar/products/", views.getSimilarProduct, name="getSimilarProduct"),
]
