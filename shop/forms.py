from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from shop.models import Product, Order, Refund


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'amount_left']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        self.user = None
        self.product = None
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product_id = self.request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(self.request, f'Product with id {product_id} does not exist')
            raise ValidationError('Product does not exist')
        user = self.request.user
        if quantity > product.amount_left:
            messages.error(self.request, f'We don\'t have so many products({product.name}) left. We have only {product.amount_left} left')
            self.add_error('quantity', ValidationError(
                'We don\'t have so many products left'))
        if quantity * product.price > user.wallet:
            messages.error(self.request, f'You need {quantity * product.price}$. But you have only {user.wallet}$')
            self.add_error('quantity', ValidationError(
                f'You need {quantity * product.price}$. But you have only {user.wallet}$'))

        self.instance.user = user
        self.instance.product = product
        return cleaned_data


class RefundForm(ModelForm):
    class Meta:
        model = Refund
        fields = ['reason']


    def __init__(self, *args, **kwargs):
        self.order = None
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        order_id = self.request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            messages.error(self.request, f'Order with id {order_id} does not exist')
            raise ValidationError('Order does not exist')
        if not order.is_refundable:
            messages.error(self.request, f'You can\'t refund this order. Time is over')
            raise ValidationError('Time is over')
        self.instance.order = order
        return cleaned_data