from rest_framework import viewsets

from shop import serializers
from .models import Product, Store, DocumentType, Document, DocumentProduct, AccessGroup
from .permissions import IsActiveUser, DocTypePermission


class ProductsAPIViews(viewsets.ModelViewSet):
    serializer_class = serializers.ProductsSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.action == 'list' and 'name' in self.request.query_params and len(self.request.query_params['name']) > 0:
            queryset = queryset.filter(name__icontains=self.request.query_params['name'])
        return queryset.order_by('name')


class StoresAPIViews(viewsets.ModelViewSet):
    serializer_class = serializers.StoresSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        queryset = Store.objects.all()
        if self.action == 'list' and 'name' in self.request.query_params and len(self.request.query_params['name']) > 0:
            queryset = queryset.filter(name__icontains=self.request.query_params['name'])
        return queryset.order_by('name')


class DocTypesAPIViews(viewsets.ModelViewSet):
    serializer_class = serializers.DocTypesSerializer
    permission_classes = [IsActiveUser]
    queryset = DocumentType.objects.all().order_by('name')
    pagination_class = None


class DocumentsAPIViews(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentsSerializer
    permission_classes = [IsActiveUser, DocTypePermission]

    def get_queryset(self):
        available_types = self.request.user.available_types
        if available_types is None:
            return Document.objects.none()
        return Document.objects.filter(doc_type_id__in=available_types).order_by('doc_date')


class DocProductAPIViews(viewsets.ModelViewSet):
    serializer_class = serializers.DocumentProductsSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        return DocumentProduct.objects.all().order_by('product__name')


class AccessGroupSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccessGroupSerializer
    permission_classes = [IsActiveUser]
    queryset = AccessGroup.objects.all().order_by('id')
