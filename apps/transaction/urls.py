from django.urls import path
from apps.transaction.views import TransactionCreate,TransactionList,TransactionApi,TransactionPDFView,TransactionListPDFView
urlpatterns = [
    path('transactions/create/',TransactionCreate.as_view(),name='transaction-create'),
    path('transactions/list/', TransactionList.as_view(),name='transaction-list'),
    path('transactions/<str:pk>/',TransactionApi.as_view()),
    path('pdf/transactions/',TransactionListPDFView.as_view()),
    path('pdf/transactions/<str:pk>/',TransactionPDFView.as_view()),
]