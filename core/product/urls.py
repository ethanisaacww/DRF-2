"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from product.views import ListProducts, ProductDetailedView, ListProductsMixins, DetailedProductMixins, ListProductsGeneric, DetailProductsGeneric, SpecialProductsGeneric
from product.views import product_list
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register(r'products', product_list, basename='product-list')

urlpatterns = [
    path('productlist/', views.listproducts, name='ListProduct'),
    path('messagelist/', views.listmessages, name='ListMessages'),
    path('classproductlist/', ListProducts.as_view(), name='ListProductClass'),
    path('classdetailedproduct/<int:pid>/', ProductDetailedView.as_view(), name='DetailedProduct'),
    path('mixinpath/', ListProductsMixins.as_view(), name='mp'),
    path('detailedmixinpath/<int:pk>/', DetailedProductMixins.as_view(), name='detailedmp'),
    path('productgenericlist/', ListProductsGeneric.as_view(), name='lpgeneric'),
    path('productgenericdetail/<int:pk>/', DetailProductsGeneric.as_view(), name='lpgenericdetail'),
    path('specialproductgeneric/', SpecialProductsGeneric.as_view(), name='specialproductgeneric'),
    ### ORM ###
    path('productlistorm/', product_list, name='product_list_orm'),
]+ router.urls
