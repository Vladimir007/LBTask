from django.contrib.auth.forms import UserCreationForm as DefUserCreationForm
from django import forms
from django.db.models import F
from .models import User, Product, Store, Document, DocumentProduct, DocumentType


class CalendarWidget(forms.TextInput):
    template_name = 'shop/calendar.html'


class UserCreationForm(DefUserCreationForm):
    class Meta(DefUserCreationForm.Meta):
        model = User
        fields = DefUserCreationForm.Meta.fields + ('patronymic',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',)


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name',)


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author")
        super().__init__(*args, **kwargs)
        self.fields['doc_type'].label = 'Document type'
        self.fields['doc_type'].queryset = self.fields['doc_type'].queryset.filter(id__in=self.author.available_types)
        self.fields['doc_date'].label = 'Document date'

        self.products_for_save = []
        self.__add_initial_for_products_field()

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all().order_by('name'), required=True,
        widget=forms.SelectMultiple(attrs={'class': 'ui multiple selection dropdown fluid', 'id': 'products_input'})
    )
    doc_date = forms.DateTimeField(required=True, input_formats=['%B %d, %Y %H:%M %p'],
                                   widget=CalendarWidget(attrs={'id': 'calendar_input', 'autocomplete': 'off'}))

    def __add_initial_for_products_field(self):
        if self.instance.id:
            self.fields["products"].initial = Product.objects.filter(documentproduct__document=self.instance)\
                .annotate(number=F('documentproduct__number')).distinct()
            for p in self.fields["products"].initial:
                self.fields["products"].widget.attrs['data-number-%s' % p.id] = p.number

    def save(self, commit=True):
        # Get number for each product
        product_numbers = {}
        for field_key in self.data:
            if field_key.startswith('product-number-'):
                product_numbers[int(field_key.replace('product-number-', ''))] = int(self.data[field_key])

        # Get products for save if there is number for it
        for doc_product in self.cleaned_data['products']:
            if doc_product.id in product_numbers:
                self.products_for_save.append(DocumentProduct(
                    product=doc_product, number=product_numbers[doc_product.id]
                ))

        if len(self.products_for_save) == 0:
            raise forms.ValidationError('Documents products list is empty')

        self.instance = super().save(False)
        self.instance.author = self.author
        if commit:
            self.instance.save()
            self.save_document_products()
        return self.instance

    def save_document_products(self):
        if not self.instance.id:
            raise ValueError('Documents products are saving before document is saved')

        for i in range(len(self.products_for_save)):
            self.products_for_save[i].document = self.instance

        DocumentProduct.objects.filter(document=self.instance).delete()
        if len(self.products_for_save) > 0:
            objs = DocumentProduct.objects.bulk_create(self.products_for_save)
            self.products_for_save = []
            return objs

        return []

    class Meta:
        model = Document
        fields = ('store', 'products', 'doc_type', 'doc_date')
        widgets = {
            'store': forms.Select(attrs={'class': 'ui selection dropdown fluid'}),
            'doc_type': forms.Select(attrs={'class': 'ui selection dropdown fluid'}),
        }


class SearchDocForm(forms.Form):
    def __init__(self, doctypes, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.fields['doc_type'].queryset = self.fields['doc_type'].queryset.filter(id__in=doctypes)

    store = forms.CharField(max_length=128, required=False)
    doc_type = forms.ModelChoiceField(empty_label='Any', required=False,
                                      queryset=DocumentType.objects.all().order_by('name'),
                                      widget=forms.Select(attrs={'class': 'ui selection dropdown fluid'}))
    doc_date_from = forms.DateTimeField(required=False, input_formats=['%B %d, %Y %H:%M %p'],
                                        widget=CalendarWidget(attrs={'id': 'doc_date_from', 'autocomplete': 'off'}))
    doc_date_to = forms.DateTimeField(required=False, input_formats=['%B %d, %Y %H:%M %p'],
                                      widget=CalendarWidget(attrs={'id': 'doc_date_to', 'autocomplete': 'off'}))
    author = forms.ModelChoiceField(queryset=User.objects.all().order_by('last_name'), required=False,
                                    widget=forms.Select(attrs={'class': 'ui selection dropdown fluid'}),
                                    empty_label='Any')

    class Meta:
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'ui selection dropdown fluid'}),
            'author': forms.Select(attrs={'class': 'ui selection dropdown fluid'}),
        }
