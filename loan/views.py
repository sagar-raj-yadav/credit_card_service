from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Loan, Payment
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer
from .tasks import calculate_credit_score, generate_billing
from django.http import  HttpResponse
from credit_card.cron import BillingCronJob 

def home_page(request):
    return HttpResponse("<h1>Hello world .This is Home page</h1>")


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calculate_credit_score(user.aadhar_id)  
            return Response({'unique_user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplyLoanView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()
            return Response({'Loan_id': loan.loan_id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MakePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def trigger_billing_cron(request):
    try:
        BillingCronJob().do()
        
        generate_billing() 
        
        return HttpResponse("Billing Cron Job executed and billing generated successfully!")
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")
