from rest_framework import serializers
from .models import User, Loan, Payment, BillingDetail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['aadhar_id', 'name', 'email', 'annual_income', 'credit_score']

    def validate_aadhar_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Aadhar ID must only contain digits.")
        if len(value) != 16:
            raise serializers.ValidationError("Aadhar ID must be exactly 16 digits.")
        return value

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Loan
        fields = ['loan_id', 'user', 'loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date']

    def validate_loan_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Loan amount must be greater than zero.")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['loan', 'payment_date', 'amount_paid']

    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2)

class BillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = ['loan', 'billing_date', 'due_date', 'min_due', 'interest_accrued', 'paid']

    min_due = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_accrued = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid = serializers.DecimalField(max_digits=10, decimal_places=2)
