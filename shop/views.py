from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from shop.forms import UserCreateForm, ProductForm, OrderForm, RefundForm
from shop.mixins import AdminPassTestMixin, NonAdminPassTestMixin, RequestToFormKwargsMixin
from shop.models import Product, Refund, Order


class ItemListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 16
    extra_context = {
        "order_form": OrderForm()
    }


class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AddProductView(AdminPassTestMixin, CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'admin/add_product.html'
    success_url = reverse_lazy('index')


class EditProductView(AdminPassTestMixin, UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'admin/edit_product.html'
    success_url = reverse_lazy('index')


class RefundListView(AdminPassTestMixin, ListView):
    model = Refund
    template_name = 'admin/refund_list.html'
    context_object_name = 'refunds'
    paginate_by = 5

    def get_queryset(self):
        return Refund.objects.select_related('order__product', 'order').all()


class MyOrderListView(NonAdminPassTestMixin, ListView):
    model = Order
    template_name = 'user/my_orders.html'
    context_object_name = 'orders'
    paginate_by = 5
    extra_context = {
        "refund_form": RefundForm()
    }

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('product', 'refund').all()


class BuyProductView(NonAdminPassTestMixin, RequestToFormKwargsMixin, CreateView):
    form_class = OrderForm
    model = Order
    http_method_names = ['post']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"You have successfully bought {form.cleaned_data['quantity']} of {self.object.product.name}")
        return response

    def form_invalid(self, form):
        return redirect('index')


class CreateRefundView(NonAdminPassTestMixin, RequestToFormKwargsMixin, CreateView):
    model = Refund
    form_class = RefundForm
    http_method_names = ['post']
    success_url = reverse_lazy('my_orders')


class ApproveRefundView(AdminPassTestMixin, DeleteView):
    model = Refund
    http_method_names = ['post']

    def form_valid(self, form):
        prepared_message = f"Refund for product {self.object.order.product.name} and quantity {self.object.order.quantity} for user {self.object.order.user.username} has been approved"
        self.object.delete(is_approved=True)
        messages.success(self.request, prepared_message)
        return redirect('refunds')


class DeclineRefundView(AdminPassTestMixin, DeleteView):
    model = Refund
    http_method_names = ['post']

    def form_valid(self, form):
        prepared_message = f"Refund for product {self.object.order.product.name} and quantity {self.object.order.quantity} for user {self.object.order.user.username} has been declined"
        self.object.delete()
        messages.success(self.request, prepared_message)
        return redirect('refunds')

