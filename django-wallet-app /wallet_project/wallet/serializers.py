from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email',
                  'password')

    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

class WalletTopUpSerializer(serializers.Serializer): #Wallet TOP-UP api wallet,amount
    wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)


    def validate(self,data):
        if data['amount'] <= 0:
            return serializers.ValidationError("Amount must be positive")

        def create(self, validated_data):
            wallet = Wallet.objects.get(id=validated_data['wallet_id'])
            wallet.balance += validated_data['amount']
            wallet.save()

            Transaction.objects.create(
                wallet= wallet,
                amount = validated_data['amount'],
                type = 'credit',
                )
            return wallet


class WalletTransferSerializer(serializers.ModelSerializer):
    from_wallet_id = serializers.IntegerField()
    to_wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)

    def validate(self,data):
        if data['amount'] <=0:
            raise serializers.ValidationError("Amount must be positive.")
        if data['from_wallet_id'] == data['to_wallet_id']:
            raise serializers.ValidationError("Cannot transfer to the same wallet")
        return data

    def create(self, validated_data):
        from_wallet = Wallet.objects.get(id=validated_data['from_wallet_id'])
        to_wallet = Wallet.objects.get(id=validated_data['to_wallet_id'])
        amount = validated_data['amount']

        if from_wallet.balance < amount:
            raise serializers.ValidationError("Insufficient Balance")

        #Perform Transfer
        from_wallet.balance -= amount
        to_wallet.balance += amount
        from_wallet.save()
        to_wallet.save()

        #Log Transactions
        Transaction.objects.create(
            wallet = from_wallet,
            amount = amount,
            type ='debit'
        )

        Transaction.objects.create(
            wallet = to_wallet,
            amount = amount,
            type = 'credit'

        )

        return {'from_wallet': from_wallet, 'to_wallet' : to_wallet}






