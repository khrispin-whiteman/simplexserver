from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
USER_TYPES = [
    ('is_borrower', 'Borrower'),
    ('is_employee', 'Employee'),
    ('is_superuser', 'Super User'),
]

LOAN_STATUS = [
    ('Requested', 'Requested'),
    ('Confirmed', 'Confirmed'),
    ('Disbursed', 'Disbursed'),
    ('Rejected', 'Rejected'),
]

OVERDUE_STATUS = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]


class User(AbstractUser):
    user_role = models.CharField('User Role', max_length=20, default='', choices=USER_TYPES)
    nrc = models.CharField(max_length=200, verbose_name='NRC', unique=True)
    phone = models.CharField(max_length=200, verbose_name='Phone Number', unique=True)
    email = models.CharField(max_length=200, verbose_name='Email Address', null=True)

    def __str__(self):
        return str(self.last_name) + ' - ' + str(self.nrc)


class Account(models.Model):
    user = models.ForeignKey(User, max_length=200, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Account Balance')

    def __str__(self):
        return str(self.user) + ' - k' + str(self.account_balance)


class LoanPlan(models.Model):
    months = models.CharField(max_length=200, verbose_name='Months')
    interest_rate = models.CharField(max_length=200, verbose_name='Interest Rate')
    penalty_rate = models.CharField(max_length=200, verbose_name='Penalty Rate')

    def __str__(self):
        return str('Months: ' + self.months + ', Interest: ' + self.interest_rate + '%, Penalty: ' + self.penalty_rate)


class LoanType(models.Model):
    loan_type_mane = models.CharField(max_length=200, verbose_name='Loan Type Name')
    loan_type_description = models.TextField('Loan Type Description', blank=True, null=True)

    def __str__(self):
        return str(self.loan_type_mane)


class Loan(models.Model):
    account = models.ForeignKey(Account, max_length=200, on_delete=models.DO_NOTHING)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Loan Amount')
    loan_type = models.ForeignKey(LoanType, max_length=200, on_delete=models.DO_NOTHING)
    loan_plan = models.ForeignKey(LoanPlan, max_length=200, on_delete=models.DO_NOTHING)
    loan_status = models.CharField(max_length=200, choices=LOAN_STATUS, default='Requested', verbose_name='Loan Status')
    ref_no = models.UUIDField('Reference Number', default=uuid.uuid4, editable=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.account.user) + ' - k' + str(self.loan_amount)


class Payment(models.Model):
    account = models.ForeignKey(Account, max_length=200, on_delete=models.DO_NOTHING)
    loan = models.ForeignKey(Loan, max_length=200, on_delete=models.DO_NOTHING)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Penalty Balance')
    overdue = models.CharField(max_length=200, choices=OVERDUE_STATUS, default='No', verbose_name='Overdue')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.account.user) + ' - ' + str(self.loan)
