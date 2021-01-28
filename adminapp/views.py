from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# categories
def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'скидка {discount}% распространяется к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# products
class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = ProductCategory.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        category_pk = self.kwargs['pk']
        success_url = reverse('adminapp:products', args=[category_pk])
        return success_url


class ProductsView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.kwargs)
        category_pk = self.kwargs['pk']
        return queryset.filter(category__pk=category_pk)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs['pk']
        product_item = get_object_or_404(ProductCategory, pk=category_pk)
        context_data['category'] = product_item
        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Product.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        product_pk = self.kwargs['pk']
        product = get_object_or_404(Product, id=product_pk)
        success_url = reverse('adminapp:products', args=[product.category_id])
        return success_url


# class ProductDeleteView(DeleteView):
#     model = Product
#     template_name = 'adminapp/product_delete.html'
#     success_url = reverse_lazy('adminapp:products')
#
#     @method_decorator(user_passes_test(lambda user: user.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if self.object.is_active:
#             self.object.is_active = False
#         else:
#             self.object.is_active = True
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda user: user.is_superuser)
# def user_create(request):
#     if request.method == "POST":
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'title': 'аутентификация',
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def users(request):
#     users_list = ShopUser.objects.all().order_by('-is_active')
#     content = {
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == "POST":
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def user_delete(request, pk):
#     user_item = get_object_or_404(ShopUser, pk=pk)
#     if request.method == "POST":
#         if user_item.is_active:
#             user_item.is_active = False
#         else:
#             user_item.is_active = True
#         user_item.save()
#         return HttpResponseRedirect(reverse('adminapp:users'))
#     content = {
#         'user_to_delete': user_item
#     }
#     return render(request, 'adminapp/user_delete.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def category_create(request):
#     if request.method == "POST":
#         category_form = ProductCategoryEditForm(request.POST)
#         if category_form.is_valid():
#             category_form.save()
#             HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {
#         'update_form': category_form
#     }
#     return render(request, 'adminapp/category_update.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     categories_list = ProductCategory.objects.all().order_by('-is_active')
#     content = {
#         'objects': categories_list
#     }
#     return render(request, 'adminapp/categories.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def category_update(request, pk):
#     category_to_update = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == "POST":
#         edit_form = ProductCategoryEditForm(request.POST, instance=category_to_update)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories', args=[category_to_update.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=category_to_update)
#
#     content = {
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/category_update.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def category_delete(request, pk):
#     category_to_delete = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == "POST":
#         if category_to_delete.is_active:
#             category_to_delete.is_active = False
#         else:
#             category_to_delete.is_active = True
#         category_to_delete.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     content = {
#         'category_to_delete': category_to_delete
#     }
#
#     return render(request, 'adminapp/category_delete.html', content)

# @user_passes_test(lambda user: user.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == "POST":
#         update_form = ProductEditForm(request.POST, request.FILES)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         update_form = ProductEditForm()
#
#     content = {
#         'update_form': update_form,
#         'category': category_item
#     }
#
#     return render(request, 'adminapp/product_update.html', content)

# @user_passes_test(lambda user: user.is_superuser)
# def products(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category=category_item)
#     content = {
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)

# @user_passes_test(lambda user: user.is_superuser)
# def product_update(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         update_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         update_form = ProductEditForm(instance=product_item)
#
#     content = {
#         'update_form': update_form,
#         'category': product_item.category
#     }
#
#     return render(request, 'adminapp/product_update.html', content)

# @user_passes_test(lambda user: user.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     content = {
#         'object': product_item
#     }
#     return render(request, 'adminapp/product_read.html', content)

@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, pk):
    product_to_delete = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        if product_to_delete.is_active:
            product_to_delete.is_active = False
        else:
            product_to_delete.is_active = True
        product_to_delete.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product_to_delete.category.id]))

    content = {
        'product_to_delete': product_to_delete
    }

    return render(request, 'adminapp/product_delete.html', content)
