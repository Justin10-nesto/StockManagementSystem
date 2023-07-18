
from django.urls import path, include
from . import views
urlpatterns = [
    path('ShopCategoryList', views.ShopCategoryList, name= 'ShopCategoryList'),
    path('EditShopCategory/<str:id>', views.EditShopCategory, name= 'EditShopCategory'),
    path('DeleteShopCategory/<str:id>', views.DeleteShopCategory, name= 'DeleteShopCategory'),
    
    path('ShopList', views.ShopList, name= 'ShopList'),
    path('EditShop/<str:id>', views.EditShop, name= 'EditShop'),
    path('DeleteShop/<str:id>', views.DeleteShop, name= 'DeleteShop'),
    
    path('ProductCategoryList', views.ProductCategoryList, name= 'ProductCategoryList'),
    path('EditProductCategory/<str:id>', views.EditProductCategory, name= 'EditProductCategory'),
    path('DeleteProductCategory/<str:id>', views.DeleteProductCategory, name= 'DeleteProductCategory'),

    path('ProductList', views.ProductList, name= 'ProductList'),
    path('EditProduct/<str:id>', views.EditProduct, name= 'EditProduct'),
    path('DeleteProduct/<str:id>', views.DeleteProduct, name= 'DeleteProduct'),

    path('ProductImportedList', views.ProductImportedList, name= 'ProductImportedList'),
    path('EditProductImported/<str:id>', views.EditProductImported, name= 'EditProductImported'),
    path('DeleteProductImported/<str:id>', views.DeleteProductImported, name= 'DeleteProductImported'),

    path('ProductSoldOutList', views.ProductSoldOutList, name= 'ProductSoldOutList'),
    path('EditProductSoldOut/<str:id>', views.EditProductSoldOut, name= 'EditProductSoldOut'),
    path('DeleteProductSoldOut/<str:id>', views.DeleteProductSoldOut, name= 'DeleteProductSoldOut'),
]
