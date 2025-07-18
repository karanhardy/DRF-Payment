from django.core.serializers import serialize
from rest_framework import generics, status, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, WalletTopUpSerializer, WalletTransferSerializer, Wallet, WalletSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet , Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger('django')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def admin_dashboard(request):
    logger.debug("Dashboard view accessed! ")
    logger.info("Dashboard view accessed! ")
    users = User.objects.all()
    wallets = Wallet.objects.select_related('User').all()
    transactions = Transaction.objects.select_related('wallet').all()

    return render(request, 'wallet/dashboard.html' ,
                  { 'users' : users,
                    'wallets' : wallets,
                    'transactions ' : transactions,})

# def dashboard(request):
#     return render(request, 'wallet/dashboard.html')

class WalletTopUpView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = WalletTopUpSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Top-Up successful"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class WalletTransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = WalletTransferSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Transfer succesful"},status = status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




