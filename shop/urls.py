from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from shop.views import ItemListView, Login, RegisterView, AddProductView, EditProductView, RefundListView, \
    MyOrderListView, BuyProductView, CreateRefundView, ApproveRefundView, DeclineRefundView

admin_urlpatterns = [
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('edit-product/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('refunds/', RefundListView.as_view(), name='refunds'),
    path('approve-refund/<int:pk>/', ApproveRefundView.as_view(), name='approve_refund'),
    path('decline-refund/<int:pk>/', DeclineRefundView.as_view(), name='decline_refund'),
]

user_urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-orders/', MyOrderListView.as_view(), name='my_orders'),
    path('buy-product/', BuyProductView.as_view(), name='buy_product'),
    path('create-refund/', CreateRefundView.as_view(), name='create_refund'),
]

urlpatterns = admin_urlpatterns + user_urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
