from django.urls import path
from .views import RegisterUserView, ApplyLoanView, MakePaymentView,home_page,trigger_billing_cron

urlpatterns = [
    path('', home_page),
    path('register-user/', RegisterUserView.as_view(), name='register-user'),
    path('apply-loan/', ApplyLoanView.as_view(), name='apply-loan'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
    path('trigger-billing-cron/', trigger_billing_cron),

]
