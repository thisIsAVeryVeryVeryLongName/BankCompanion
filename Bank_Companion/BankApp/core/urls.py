
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.start_page, name="start_page"),
    path('account-list/', views.account_list_view, name='account_list_view'),
    path('edit-account-list/', views.edit_account_list_view, name='edit_account_list_view'),
    path('create-account/', views.create_account_view, name='create_account_view'),
    path('account-add-money/<int:account_pk>/', views.account_add_money_view, name='account_add_money'),
    path('account-sub-money/<int:account_pk>/', views.account_sub_money_view, name='account_sub_money'),
    path('unasigned-transaction/', views.unasigned_transaction_view, name='unasigned_transactions'),
    path('unasigned-transaction/asign/', views.asign_unasigned_transactions, name='asign_unasigned_transactions'),
    path('outgoing-transaction-list/', views.outgoing_transaction_list_view, name='outgoing_transaction_list_view'),
    path('transaction-detail/', views.update_transaction, name='update_transaction'),
    path('transaction-detail/<int:pk>/', views.transaction_detail_view, name='transaction_detail_view'),
    path('incoming-transaction-list/', views.incoming_transaction_list_view, name='incoming_transaction_list_view'),
    path('make-transaction/', views.make_transaction_view, name='make_transaction_view'),
    path('submit-make-transaction/', views.submit_make_transaction_view, name='submit_make_transaction_view'),
    path('sharing-group-list/', views.sharing_group_list_view, name='sharing_group_list_view'),
    path('create-sharing-group/', views.create_sharing_group_view, name='create_sharing_group_view'),
    path('submit-create-sharing-group/', views.submit_create_sharing_view, name='submit_create_sharing_view'),
    path('sharing-group-detail/<int:pk>', views.sharing_group_detail_view, name='sharing_group_detail_view'),
    path('sharing-spendings-detail/<int:pk>', views.sharing_spendings_detail_view, name='sharing_spendings_detail_view'),
    path('create-sharing-spendings/<int:pk>', views.create_sharing_spendings_view, name='create_sharing_spendings_view'),
    path('submit-sharing-spendings/<int:pk>', views.submit_sharing_spendings_view, name='submit_sharing_spendings_view'),
    path('sharing-spendings-balance-transaction/<int:group_pk>/', views.sharing_make_transaction, name='sharing_make_transaction'),
    path('sharing-spendings-balance/<int:pk>', views.sharing_spendings_balance_view, name='sharing_spendings_balance_view'),
    path('fpm/', views.fpm_view, name='fpm_view'),
    

    path('api/make-transaction/', views.api_make_transaction_view, name='api_make_transaction_view'),
    
]
