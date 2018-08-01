from rest_framework import serializers
from .models import Product, Store, DocumentType, Document, DocumentProduct, AccessGroup


class ModelMultipleChoiceField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.display_field = kwargs.pop("display_field", "name")
        super().__init__(**kwargs)

    def display_value(self, instance):
        # Use a specific field rather than model stringification
        return getattr(instance, self.display_field)


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'url', 'name', 'date_changed', 'date_created')


class StoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'url', 'name', 'date_changed', 'date_created')


class DocTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'date_changed', 'date_created')


class DocumentProductsSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(min_value=1)

    class Meta:
        model = DocumentProduct
        fields = ('document', 'product', 'number')


class DocumentsSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            kwargs['author'] = request.user
        else:
            raise serializers.ValidationError('Request is without user')
        return super().save(**kwargs)

    class Meta:
        model = Document
        fields = ('id', 'url', 'store', 'doc_type', 'doc_date', 'author', 'date_created', 'date_changed')
        extra_kwargs = {'url': {'view_name': 'shop:documents-detail'}}
        read_only_fields = ('author',)


class AccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessGroup
        fields = '__all__'
