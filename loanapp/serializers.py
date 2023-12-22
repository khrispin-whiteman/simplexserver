from rest_framework import serializers
from loanapp.models import User, Account, Payment, LoanPlan, LoanType, Loan
from django.contrib.auth import authenticate


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'nrc', 'phone', 'email', 'user_role', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'user', 'account_balance', 'date_created')


class LoanPlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoanPlan
        fields = ('id', 'months', 'interest_rate', 'penalty_rate')


class LoanTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LoanType
        fields = ('id', 'loan_type_mane', 'loan_type_description')


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'account', 'loan_amount', 'loan_type', 'loan_plan', 'loan_status', 'ref_no', 'date_created')


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
