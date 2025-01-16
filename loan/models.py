from django.db import models
from uuid import uuid4
from decimal import Decimal

class User(models.Model):
    aadhar_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=15, decimal_places=2)
    credit_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [('credit_card', 'Credit Card')]

    loan_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    principal_due = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    interest_due = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan ID: {self.loan_id}"

class BillingDetail(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    due_date = models.DateField()
    min_due = models.DecimalField(max_digits=10, decimal_places=2)
    interest_accrued = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Billing for Loan ID: {self.loan.loan_id} on {self.billing_date}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Loan ID {self.loan.loan_id} on {self.payment_date}"
