from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, ListView

from .models import Product, Store, Document
from .forms import ProductForm, StoreForm, DocumentForm, SearchDocForm
from .utils import DocTypeAccessMixin
from .raw_sqls import DocumentsListSQL


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProductsHome(LoginRequiredMixin, TemplateView):
    template_name = 'shop/products.html'


class InspectProductView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shop/product_crud/details.html'


class CreateProductView(LoginRequiredMixin, CreateView):
    template_name = 'shop/product_crud/form.html'
    form_class = ProductForm
    success_url = reverse_lazy('shop:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Create'
        context['title'] = 'New Product'
        context['back_url'] = reverse('shop:products')
        return context


class EditProductView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/product_crud/form.html'
    form_class = ProductForm
    success_url = reverse_lazy('shop:products')
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Save'
        context['title'] = 'Edit Product'
        context['back_url'] = reverse('shop:product', args=[self.object.id])
        return context


class DeleteProductView(LoginRequiredMixin, DeleteView):
    template_name = 'shop/product_crud/delete.html'
    model = Product
    success_url = reverse_lazy('shop:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Delete'
        context['title'] = 'Product deletion'
        context['back_url'] = reverse('shop:product', args=[self.object.id])
        return context


class StoresHome(LoginRequiredMixin, TemplateView):
    template_name = 'shop/stores.html'


class InspectStoreView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = 'shop/store_crud/details.html'


class CreateStoreView(LoginRequiredMixin, CreateView):
    template_name = 'shop/store_crud/form.html'
    form_class = StoreForm
    success_url = reverse_lazy('shop:stores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Create'
        context['title'] = 'New Store'
        context['back_url'] = reverse('shop:stores')
        return context


class EditStoreView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/store_crud/form.html'
    form_class = StoreForm
    success_url = reverse_lazy('shop:stores')
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Save'
        context['title'] = 'Edit Store'
        context['back_url'] = reverse('shop:store', args=[self.object.id])
        return context


class DeleteStoreView(LoginRequiredMixin, DeleteView):
    template_name = 'shop/store_crud/delete.html'
    model = Store
    success_url = reverse_lazy('shop:stores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Delete'
        context['title'] = 'Store deletion'
        context['back_url'] = reverse('shop:store', args=[self.object.id])
        return context


class DocumentsList(LoginRequiredMixin, ListView):
    template_name = 'shop/documents.html'
    paginate_by = 15
    model = Document

    def get_queryset(self):
        filters = {}
        available_types = self.request.user.available_types
        if available_types is None:
            return self.model.objects.none()
        filters['doc_type_id__in'] = available_types

        self.search_form = SearchDocForm(filters['doc_type_id__in'], self.request.GET)

        queryset_kwargs = {}
        if self.search_form.is_valid():
            queryset_kwargs = self.search_form.cleaned_data

        return list(DocumentsListSQL(self.request.user, **queryset_kwargs).queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'search_form'):
            context['search_form'] = self.search_form
        return context


class InspectDocumentView(LoginRequiredMixin, DocTypeAccessMixin, DetailView):
    model = Document
    template_name = 'shop/document_crud/details.html'


class CreateDocumentView(LoginRequiredMixin, DocTypeAccessMixin, CreateView):
    template_name = 'shop/document_crud/form.html'
    form_class = DocumentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('shop:document', self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Create'
        context['title'] = 'New Document'
        context['back_url'] = reverse('shop:documents')
        return context


class EditDocumentView(LoginRequiredMixin, DocTypeAccessMixin, UpdateView):
    template_name = 'shop/document_crud/form.html'
    form_class = DocumentForm
    model = Document

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('shop:document', self.object.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Save'
        context['title'] = 'Edit Document'
        context['back_url'] = reverse('shop:document', args=[self.object.id])
        return context


class DeleteDocumentView(LoginRequiredMixin, DocTypeAccessMixin, DeleteView):
    template_name = 'shop/document_crud/delete.html'
    model = Document
    success_url = reverse_lazy('shop:documents')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['submit_btn'] = 'Delete'
        context['title'] = 'Document deletion'
        context['back_url'] = reverse('shop:document', args=[self.object.id])
        return context
