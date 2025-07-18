from django.contrib import admin
from  .models import Wallet , Transaction

class WalletAdmin(admin.ModelAdmin):
    list_display  = ('user', 'balance')
    def log_addition(self,request,obj,message):
        #overriding log message to user str(obj)
        super().log_addition(request,obj,message or str(obj))



class TransactionAdmin(admin.ModelAdmin):
    list_display  = ('wallet', 'amount','type','timestamp')
    def log_addition(self,request,obj,message):
        #overriding log message to user str(obj)
        super().log_addition(request,obj,message or str(obj))

admin.site.register(Wallet,WalletAdmin)
admin.site.register(Transaction,TransactionAdmin)