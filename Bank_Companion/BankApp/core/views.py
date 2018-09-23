from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import VirtualBankAccount, BankAccount, Transaction, SharingGroup, TagIndex, SharingInfo, SharingSpending
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from .forms import TransactionForm, TransactionAPIForm, SharingGroupForm,PdfForm, AmountForm, CreateSpendingsForm,CreateAccountForm
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime, timedelta
from .open_hub import OpenHub
from .kilians_index import KiliansIndex

# Create your views here.
@login_required(login_url='/accounts/login/')
def start_page(request):
    return redirect('/account-list/')

@login_required(login_url='/accounts/login/')
def account_list_view(request):
    if request.method == 'POST':
        accounts = VirtualBankAccount.get_by_user(request.user)
        default_account = BankAccount.objects.get(owner=request.user)
        print(accounts)
        return render(request, 'core/accounts/account_list.html', {'accounts':accounts,'default_account':default_account})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')


@login_required(login_url='/accounts/login/')
def create_account_view(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST if request.POST else None)
        if(form.is_valid()):
            form.save(request.user)
            return HttpResponseRedirect(reverse('core:account_list_view'))
        return render(request, 'core/accounts/create_account.html', {'form': form})

    return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def transaction_detail_view(request, pk):
    if request.method == 'POST':
        t = get_object_or_404(Transaction, pk=pk)
        accounts = VirtualBankAccount.get_by_user(request.user)
        return render(request, 'core/transactions/transaction_detail.html', {'t':t, 'accounts':accounts})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')       
def update_transaction(request):
    if request.method == 'POST':
        t = get_object_or_404(Transaction, pk=request.POST.get('transaction_id', None))
        t.virtual_bank = get_object_or_404(VirtualBankAccount, pk=request.POST.get('pk', None))
        t.save()
        if t.is_outgoing(request.user):
            return redirect('/outgoing-transaction-list/')
        else:
            return redirect('/incoming-transaction-list/')

    if request.method == 'GET':
        return render(request, 'core/base_core.html')


    
@login_required(login_url='/accounts/login/')
def unasigned_transaction_view(request):
    if request.method == 'POST':
        transactions = Transaction.objects.filter(is_assigned=False)
        oh=KiliansIndex.get_connection()
        for t in transactions:
            i=TagIndex.getIcon(request.user,t.iban)
            if(i!=None):
                vba=VirtualBankAccount.objects.all().filter(bank_account__owner=request.user,icon=i)
                if(vba):
                    vba=vba[0]
                    t.virtual_bank=vba
                    t.is_assigned=True
                    print(t,'assigned TRUE')
                    t.save()
            else:
                KiliansIndex.apply(oh,t,request.user)
            t.is_assigned = True
            t.save()

        transactions = Transaction.objects.filter(is_assigned=False)
        if not transactions:
            return HttpResponse('none')
        else:
            accounts = VirtualBankAccount.get_by_user(request.user)
            return render(request, 'core/transactions/transactions.html',{'transactions':transactions, 'accounts':accounts})

    if request.method == 'GET':
        return redirect('/account-list/')




@login_required(login_url='/accounts/login/')
def outgoing_transaction_list_view(request):
    if request.method == 'POST':
        transactions = Transaction.get_by_user(request.user)
        default_account = BankAccount.objects.get(owner=request.user)
        dt1=datetime.today() - timedelta(days=30)
        this_month=Transaction.objects.all().filter(created_at__gte=dt1,bank_account=default_account)
        sum=0
        for t in this_month:
            if(t.is_outgoing(request.user)):
                print('add: ',t.amount)
                sum=sum+t.amount
        p=(sum/default_account.money_out_last_month)*100
        color='#e23c3c'
        if(p>=100):
            color='#0ba070'
        elif(p>=85):
            color='#d6bc06'
        print(p)
        percentage_width=min(p/2,100)
        p=p-100
        return render(request, 'core/transactions/transaction_list_outgoing.html', {'transactions':transactions,'title':'Outgoing Transactions','money_sum':sum,'percentage_sum':p,'percentage_color':color,'percentage_width':percentage_width})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')


@login_required(login_url='/accounts/login/')
def incoming_transaction_list_view(request):
    if request.method == 'POST':
        transactions = Transaction.get_by_recipient(request.user)
        default_account = BankAccount.objects.get(owner=request.user)
        dt1=datetime.today() - timedelta(days=30)
        this_month=Transaction.objects.all().filter(created_at__gte=dt1,iban=default_account.iban)
        sum=0
        for t in this_month:
            if(t.is_incomming(request.user)):
                print('add: ',t.amount)
                sum=sum+t.amount
        p=(sum/default_account.money_in_last_month)*100
        color='#e23c3c'
        if(p>=100):
            color='#0ba070'
        elif(p>=85):
            color='#d6bc06'
        percentage_width=min(p/2,100)
        p=p-100
        return render(request, 'core/transactions/transaction_list_incoming.html', {'transactions':transactions,'title':'Incoming Transactions','money_sum':sum,'percentage_sum':p,'percentage_color':color,'percentage_width':percentage_width})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def make_transaction_view(request):
    if request.method == 'POST':
        if(not request.POST):
            form = TransactionForm(None,user=request.user)
        else:
            form = TransactionForm(request.POST,user=request.user)

        pdf_form = PdfForm(request.POST or None,request.FILES or None)
            
        return render(request, 'core/transactions/make_transaction_form.html', {'form':form,'pdf_form':pdf_form})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def submit_make_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST,user=request.user)
        pdf_form = PdfForm(request.POST,request.FILES)
        print(form.is_valid())
        print(pdf_form.is_valid())
        if(form.is_valid()):
            form.save(request.user)
            return HttpResponseRedirect(reverse('core:outgoing_transaction_list_view'))
        elif (pdf_form.is_valid()):
            text = pdf_form.process_image()
            text=text.lower()
            text.find('iban')
            iban='IT60 X054 2811 1010 0000 0123 456'
            description=''
            bic=''
            recipient=''
            amount=200.56
            form = TransactionForm({'iban':iban,'description':description,'bic':bic,'recipient':recipient,'amount':amount},user=request.user)
        else:
            form = TransactionForm(None,user=request.user)
        return render(request, 'core/transactions/make_transaction_form.html', {'form':form,'pdf_form':pdf_form})
    
    return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def fpm_view(request):
    if request.method == 'POST':
        accounts = VirtualBankAccount.get_by_user(request.user)
        default_account = BankAccount.objects.get(owner=request.user)
        
        return render(request, 'core/fpm/fpm_list.html',{'accounts':accounts,'default_account':default_account})
        

    return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def account_add_money_view(request,account_pk):
    if request.method == 'POST':
        va = get_object_or_404(VirtualBankAccount,pk=account_pk)
        form = AmountForm(request.POST);
        
        if(form.is_valid()):
            print(form.get_amount())
            va.move_money_to_default(form.get_amount())

    return HttpResponse(status=204)

@login_required(login_url='/accounts/login/')
def account_sub_money_view(request,account_pk):
    if request.method == 'POST':
        va = get_object_or_404(VirtualBankAccount,pk=account_pk)
        form = AmountForm(request.POST);
        if(form.is_valid()):
            print(form.get_amount())
            va.move_money_to_default(-form.get_amount())

    return HttpResponse(status=204)


@login_required(login_url='/accounts/login/')
def edit_account_list_view(request):
    if request.method == 'POST':
        accounts = VirtualBankAccount.get_by_user(request.user)
        default_account = BankAccount.objects.get(owner=request.user)
        
        return render(request, 'core/accounts/edit_account_list.html',{'accounts':accounts,'default_account':default_account}) 


    return render(request, 'core/base_core.html')


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status , generics , mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

@api_view(['POST'])
def api_make_transaction_view(request):
    if request.method == 'POST':
        form=TransactionAPIForm(request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponse("OK")
        else:
            return HttpResponse("ERROR")
    return HttpResponse("Only post",code=404)
    
@login_required(login_url='/accounts/login/')
def asign_unasigned_transactions(request):
    if request.method == 'POST':
        try:
            transaction = Transaction.objects.filter(pk=request.POST.get('transaction_id', None)).first()
            transaction.is_assigned = True
            account = VirtualBankAccount.objects.filter(pk=request.POST.get('pk', None)).first()
            transaction.virtual_bank = account
            account.add_money(transaction.amount,complete=False)
            transaction.save()
            TagIndex.make(request.user,transaction.iban,account.icon)
            return redirect('/account-list/')
        except Exception as e:
            return redirect('/account-list/')

    if request.method == 'GET':
        return redirect('/account-list/')



#Schmella Code Money Sharing
@login_required(login_url='/accounts/login/')
def sharing_group_list_view(request):
    if request.method == 'POST':
        sharing_group = SharingGroup.objects.filter(owner=request.user)
        sharing_info = SharingInfo.objects.filter(user=request.user)
        has_groups=False
        if(sharing_info):
            has_groups=True
        return render(request, 'core/sharing/sharing_group_list.html', {'sharing_info':sharing_info, 'has_groups':has_groups})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def create_sharing_group_view(request):
    if request.method == 'POST':
        form = SharingGroupForm(None)
            
        return render(request, 'core/sharing/create_sharing_form.html', {'form':form})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def submit_create_sharing_view(request):
    if request.method == 'POST':
        form = SharingGroupForm(request.POST)
        if(form.is_valid()):
            form.save(request.user)
            return HttpResponseRedirect(reverse('core:sharing_group_list_view'))
    
    return HttpResponse(status=204)

@login_required(login_url='/accounts/login/')
def sharing_group_detail_view(request, pk): #users view
    if request.method == 'POST':       
        sharing_group = get_object_or_404(SharingGroup, pk=pk)
        sharing_info = SharingInfo.objects.filter(sharing_group=sharing_group)

        return render(request, 'core/sharing/sharing_group_detail.html', {'sharing_group':sharing_group, 'sharing_info':sharing_info})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

  
@login_required(login_url='/accounts/login/')
def sharing_spendings_detail_view(request, pk):
    if request.method == 'POST':       
        sharing_group = get_object_or_404(SharingGroup, pk=pk)
        sharing_spendings = SharingSpending.objects.filter(sharing_group=sharing_group)
        return render(request, 'core/sharing/sharing_spendings_detail.html', {'sharing_group':sharing_group, 'sharing_spendings':sharing_spendings})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')


@login_required(login_url='/accounts/login/')
def create_sharing_spendings_view(request, pk):
    sharing_group = get_object_or_404(SharingGroup, pk=pk)
    if request.method == 'POST':
        form = CreateSpendingsForm(None)
        return render(request, 'core/sharing/create_spendings_form.html', {'form':form, 'sharing_group':sharing_group})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')

@login_required(login_url='/accounts/login/')
def submit_sharing_spendings_view(request, pk):
    if request.method == 'POST':
        #info = SharingInfo.objects.filter(sharing_group=SharingGroup.objects.filter(pk=pk).first()).first()
        form = CreateSpendingsForm(request.POST)
        info = SharingInfo.objects.filter(user=request.user, sharing_group=SharingGroup.objects.get(pk=pk)).first()
        if(form.is_valid()):
            form.save(info, pk, info)
            return HttpResponseRedirect(reverse('core:sharing_spendings_detail_view', kwargs={'pk': pk}))
    
    return HttpResponse(status=204)

@login_required(login_url='/accounts/login/')
def sharing_spendings_balance_view(request, pk):
    if request.method == 'POST':       
        sharing_group = get_object_or_404(SharingGroup, pk=pk)
        sharing_info = SharingInfo.objects.filter(sharing_group=sharing_group)
        sharing_spendings = SharingSpending.objects.filter(sharing_group=sharing_group)
        user,amount,avg=SharingSpending.get_triple(sharing_group)
        l=[]
        for i in range(0,len(user)):
            l.append((user[i],amount[i]))
        return render(request, 'core/sharing/sharing_spendings_balance.html', {'sharing_group':sharing_group, 'sharing_spendings':sharing_spendings, 'balance_list':l})

    if request.method == 'GET':
        return render(request, 'core/base_core.html')


def sharing_make_transaction(request,group_pk):
    if request.method == 'POST':
        sharing_group = get_object_or_404(SharingGroup, pk=group_pk)
        SharingSpending.transaction(sharing_group)

        #set all at 0
        people=SharingInfo.objects.all().filter(sharing_group=sharing_group)
        for p in people:
            ss=SharingSpending.objects.all().filter(paying_user=p)
            for s in ss:
                s.delete()

        return HttpResponseRedirect(reverse('core:sharing_spendings_detail_view',kwargs={'pk':group_pk}))

    return HttpResponse(status=204)


