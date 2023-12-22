from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from  django.core.serializers import serialize
from datetime import date
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
#################
from loanapp.models import User, Account, LoanPlan, LoanType, Loan, Payment
from loanapp.serializers import (UserSerializer, LoginSerializer, AccountSerializer, LoanPlanSerializer,
                                 LoanTypeSerializer, LoanSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'first_name', 'last_name', 'nrc', 'phone', 'email')


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'user', 'account_balance', 'date_created')


class LoanPlanViewSet(viewsets.ModelViewSet):
    queryset = LoanPlan.objects.all().order_by('id')
    serializer_class = LoanPlanSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'months', 'interest_rate', 'penalty_rate')


class LoanTypeViewSet(viewsets.ModelViewSet):
    queryset = LoanType.objects.all().order_by('id')
    serializer_class = LoanTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'loan_type_mane', 'loan_type_description')


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('id')
    serializer_class = LoanSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('id', 'account', 'loan_amount', 'loan_type', 'loan_plan', 'loan_status', 'ref_no', 'date_created')


def userdata(request, user_id):
    # get user data
    data = User.objects.get(id=user_id)

    # serialize the object to json
    serialized_data = serialize('json', [data])

    print(serialized_data)
    return serialized_data
    # return JsonResponse(serialized_data, safe=False)


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        return Response(userdata(request, user.id), status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "Logout Successful"})

    def post(self, request):
        logout(request)
        return Response({"message": "Logout Successful"})