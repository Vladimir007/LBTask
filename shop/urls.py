from django.urls import path, include
from rest_framework import routers

from shop import api_views as api
from shop import views


router = routers.DefaultRouter()
router.register('products', api.ProductsAPIViews, 'products')
router.register('stores', api.StoresAPIViews, 'stores')
router.register('doctypes', api.DocTypesAPIViews, 'doctypes')
router.register('docproducts', api.DocProductAPIViews, 'docproducts')
router.register('documents', api.DocumentsAPIViews, 'documents')
router.register('accessgroup', api.AccessGroupSet, 'accessgroup')


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('shop-api/', include(router.urls)),

    path('products/', views.ProductsHome.as_view(), name='products'),
    path('products/create/', views.CreateProductView.as_view(), name='create_product'),
    path('products/details/<int:pk>/', views.InspectProductView.as_view(), name='product'),
    path('products/edit/<int:pk>/', views.EditProductView.as_view(), name='edit_product'),
    path('products/delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),

    path('stores/', views.StoresHome.as_view(), name='stores'),
    path('stores/create/', views.CreateStoreView.as_view(), name='create_store'),
    path('stores/details/<int:pk>/', views.InspectStoreView.as_view(), name='store'),
    path('stores/edit/<int:pk>/', views.EditStoreView.as_view(), name='edit_store'),
    path('stores/delete/<int:pk>/', views.DeleteStoreView.as_view(), name='delete_store'),

    path('documents/', views.DocumentsList.as_view(), name='documents'),
    path('documents/create/', views.CreateDocumentView.as_view(), name='create_document'),
    path('documents/details/<int:pk>/', views.InspectDocumentView.as_view(), name='document'),
    path('documents/edit/<int:pk>/', views.EditDocumentView.as_view(), name='edit_document'),
    path('documents/delete/<int:pk>/', views.DeleteDocumentView.as_view(), name='delete_document'),
]
