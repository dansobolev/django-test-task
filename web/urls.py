from django.urls import path
from .views import (
    FileUploadView, ListGoodsBoughtByCustomer, ListShopsByCustomer,
    ListGoodIntervalDate, ListBillsWithGoodsWithingDataIntervals
)


urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('customer-goods/<customer_id>', ListGoodsBoughtByCustomer.as_view()),
    path('customer-shops/<customer_id>', ListShopsByCustomer.as_view()),
    path('goods-sum-interval/<customer_id>', ListGoodIntervalDate.as_view()),
    path('list-bills-goods/<customer_id>', ListBillsWithGoodsWithingDataIntervals.as_view())
]
