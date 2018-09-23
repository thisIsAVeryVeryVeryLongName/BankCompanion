from django import forms
from django.forms import ModelForm
from .models import *
import requests
from .pdf import *
import os
from .kilians_index import KiliansIndex



class TransactionForm(forms.Form):
    recipient = forms.CharField(max_length=255,required=True)
    description = forms.CharField(max_length=255,required=True)
    iban = forms.CharField(max_length=255,required=True)
    bic = forms.CharField(max_length=255,required=True)
    amount = forms.FloatField(initial=0.0,required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['source_account'] = forms.ModelChoiceField(VirtualBankAccount.get_by_user(user),required=False, empty_label="Default", initial=None)
    
    def save(self, user):
        print(self.fields.keys())
        ba=BankAccount.objects.get(owner=user)
        t=Transaction(description=self.cleaned_data['description'], recipient=self.cleaned_data['recipient'],  iban=self.cleaned_data['iban'],bic=self.cleaned_data['bic'], amount=self.cleaned_data['amount'], bank_account=ba, is_assigned=False)
        t.save()
        if(self.cleaned_data['source_account']):
            self.cleaned_data['source_account'].sub_money(self.cleaned_data['amount'],complete=True);
            TagIndex.make(user,self.cleaned_data['iban'],self.cleaned_data['source_account'].icon);
        else:
            oh=KiliansIndex.get_connection()
            if(not KiliansIndex.apply(oh,t,user)):
                ba.sub_money_from_default_virtual_account(self.cleaned_data['amount'])
                i=ba.icon()
                TagIndex.make(user,self.cleaned_data['iban'],i)
        try:
            r = requests.post("http://172.31.201.167/api/transfer", data={'amount': t.amount, 'text': t.description, 'iban': t.iban})
            print(r.status_code, r.reason)
        except:
            pass


class PdfForm(forms.Form):
    file = forms.FileField(required=True)

    def process_image(self):
        text= textFromPdf(self.cleaned_data['file'])
        return text

    def is_valid(self):
        if(not super().is_valid()):
            return False
        print(self.cleaned_data['file'].name)
        print(self.cleaned_data['file'].name.lower()+"'")
        print(self.cleaned_data['file'].name.lower().endswith('.pdf'))
        return self.cleaned_data['file'].name.lower().endswith('.pdf')

class AmountForm(forms.Form):
    amount = forms.FloatField(initial=100.0,required=True)
    
    def get_amount(self):
        return self.cleaned_data['amount']

class CreateAccountForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    icon = forms.ModelChoiceField(queryset=Icon.objects.all(),required=False, empty_label="None", initial=None)

    def is_valid(self):
        tmp=super().is_valid()
        for key in ['name','icon']:
            if(key not in self.data):
                return False        
        return tmp

    def save(self, user):
        vb=VirtualBankAccount()
        vb.name=self.cleaned_data['name']
        vb.icon = self.cleaned_data['icon']
        vb.bank_account=BankAccount.objects.get(owner=user)
        vb.save()




class TransactionAPIForm(forms.Form):
    recipient = forms.CharField(max_length=255,required=True)
    description = forms.CharField(max_length=255,required=True)
    iban = forms.CharField(max_length=255,required=True)
    amount = forms.FloatField(initial=0.0,required=True)
    
    def save(self, user):
        print("Transaction to '"+self.cleaned_data['recipient']+"' with IBAN '"+self.cleaned_data['iban']+"' and description '"+self.cleaned_data['description']+"' and an amount of "+self.cleaned_data['amount']+"€");



#Schmella Code Sharing Groups
class SharingGroupForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    
    def save(self, user):
        print(self.fields.keys())
        sg=SharingGroup(name=self.cleaned_data['name'],owner=user)
        sg.save()


class CreateSpendingsForm(forms.Form):
    price = forms.FloatField(required = True)
    description = forms.CharField(max_length=255, required = False)
    
    def save(self, user, pk, info):
        print(self.fields.keys())
        sg=SharingSpending(price=self.cleaned_data['price'], description=self.cleaned_data['description'], paying_user=info, sharing_group=SharingGroup.objects.filter(pk=pk).first())
        sg.save()
