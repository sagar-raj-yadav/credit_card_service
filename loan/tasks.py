import csv
from datetime import datetime, timedelta
from .models import User, Loan, BillingDetail, Payment

def calculate_credit_score(aadhar_id):
    try:
        user = User.objects.get(aadhar_id=aadhar_id)
        transaction_file = "transaction.csv"

        total_credit = 0
        total_transactions = 0

        with open(transaction_file, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row['AadharID'] == aadhar_id and row['TransactionType'] == 'credit':
                    total_credit += float(row['TransactionAmount'])
                    total_transactions += 1

        if total_transactions == 0:
            user.credit_score = 0
        else:
            user.credit_score = min(900, 300 + int((total_credit / total_transactions) * 5))

        user.save()
        print(f"Credit score for Aadhar ID {aadhar_id} updated to {user.credit_score}")

    except User.DoesNotExist:
        print(f"User with Aadhar ID {aadhar_id} does not exist.")
    except Exception as e:
        print(f"Error calculating credit score: {e}")

def generate_billing():
    try:
        loans = Loan.objects.filter(is_closed=False)
        billing_details = []

        for loan in loans:
            today = datetime.now().date()
            next_billing_date = today + timedelta(days=30)

            interest_accrued = (loan.loan_amount * loan.interest_rate / 100) / 12
            min_due = interest_accrued

            billing_details.append(
                BillingDetail(
                    loan=loan,
                    billing_date=today,
                    due_date=next_billing_date,
                    min_due=min_due,
                    interest_accrued=interest_accrued
                )
            )

        BillingDetail.objects.bulk_create(billing_details)
        print(f"Generated {len(billing_details)} billing records.")

    except Exception as e:
        print(f"Error generating billing: {e}")

def process_transaction_file():
    try:
        transaction_file = "transaction.csv"

        with open(transaction_file, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                aadhar_id = row['AadharID']
                transaction_type = row['TransactionType']
                payment_date = datetime.strptime(row['PaymentDate'], '%Y-%m-%d').date()
                amount_paid = float(row['TransactionAmount'])

                if transaction_type in ['credit', 'debit']:
                    try:
                        user = User.objects.get(aadhar_id=aadhar_id)
                        loan = Loan.objects.filter(user=user, is_closed=False).first()

                        if loan and transaction_type == 'credit':
                            Payment.objects.create(
                                loan=loan,
                                payment_date=payment_date,
                                amount_paid=amount_paid,
                            )
                            print(f"Payment recorded for Loan ID {loan.loan_id}")
                        elif not loan:
                            print(f"No active loan found for User {user.name}.")
                        else:
                            print(f"Skipping debit transaction for Loan ID {loan.loan_id}")

                    except User.DoesNotExist:
                        print(f"User with Aadhar ID {aadhar_id} does not exist.")
                else:
                    print(f"Invalid transaction type or missing data for row: {row}")

    except Exception as e:
        print(f"Error processing transaction file: {e}")
