from core.models import *
from django.contrib.auth.models import User

def run():
        #Add FontAwesome
    Icon.objects.all().delete()
    print("Add FontAwesome")

    fa = Icon.objects.create()
    fa.name = "Food"
    fa.icon = 'fas fa-utensils'
    fa.avg_output = '300'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Vacation"
    fa.icon = 'fas fa-plane'
    fa.avg_output = '1000'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Car"
    fa.icon = 'fas fa-car-alt'
    fa.avg_output = '300'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Savings"
    fa.icon = 'fas fa-piggy-bank'
    fa.avg_output = '100'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Online Shopping"
    fa.icon = 'fas fa-shopping-cart'
    fa.avg_output = '150'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Bills"
    fa.icon = 'fas fa-file-invoice-dollar'
    fa.avg_output = '300'
    fa.save()

    fa = Icon.objects.create()
    fa.name = "Default"
    fa.icon = 'fas fa-globe'
    fa.avg_output = '300'
    fa.save()

    #Create Users
    User.objects.all().delete()
    print("Create Users")
    u = User.objects.create()
    u.username = "superuser"
    u.firstname = "Admin"
    u.lastname = "Istrator"
    u.email = "example@example.com"        
    u.is_superuser = True
    u.is_staff = True
    u.password = "amadeuspeniss"
    u.save()

    u = User.objects.create_user("client1",password = "amadeuspeniss")
    u.first_name = "Kilian"
    u.last_name = "Hinteregger"
    u.email = "example@example.com"  
    u.save()

    u = User.objects.create_user("client2",password = "amadeuspeniss")
    u.first_name = "David"
    u.last_name = "Gatta"
    u.email = "example@example.com" 
    u.save()

    u = User.objects.create_user("client3",password = "amadeuspeniss")
    u.first_name = "Martin"
    u.last_name = "Kofler"
    u.email = "example@example.com"        #optional
    u.save()

    print("  Create User 'admin'")
    user=User.objects.create_user('admin', password='amadeuspeniss')
    user.first_name='Admin'
    user.last_name='Istartor'
    user.is_superuser=True
    user.is_staff=True
    user.save()

    #Create Bank Accounts
    print("Create Bank Accounts")
    BankAccount.objects.all().delete()
    b = BankAccount.objects.create(owner=User.objects.get(username="client1"))
    b.account_number = 1
    b.balance = 2000.00
    b.iban = "IT60 X111 1111 1110 0000 0111 111"
    b.bic = "RZSBIT21007"
    b.money_sub_month = 1200
    b.save()

    b = BankAccount.objects.create(owner=User.objects.get(username="client2"))
    b.account_number = 2
    b.balance = 5000.00    
    b.iban = "IT60 X222 2222 2220 0000 0222 222"
    b.bic = "RZSBIT21105"
    b.money_sub_month = 1600
    b.save()

    b = BankAccount.objects.create(owner=User.objects.get(username="client3"))
    b.account_number = 3
    b.balance = 13421.00
    b.iban = "IT60 X333 3333 3330 0000 0333 333"
    b.bic = "RZSBIT21105"
    b.money_sub_month = 1000
    b.save()
    

    #Create VirtualBankAccounts
    print("Create Virtual Bank Accounts")
    VirtualBankAccount.objects.all().delete()

    vb1 = VirtualBankAccount.objects.create(bank_account = BankAccount.objects.get(account_number=1))     #BAcc1 VBA1
    vb1.name = "Food"
    vb1.balance = 200.00
    vb1.money_sub_month = 400
    vb1.icon = Icon.objects.filter(name="Food").first()
    vb1.save()

    vb2 = VirtualBankAccount.objects.create(bank_account = BankAccount.objects.get(account_number=1))     #BAcc1 VBA2
    vb2.name = "Holiday"
    vb2.balance = 300
    vb2.money_sub_month = 100
    vb2.icon = Icon.objects.filter(name="Vacation").first()
    vb2.save()

    vb3 = VirtualBankAccount.objects.create(bank_account = BankAccount.objects.get(account_number=1))     #BAcc2 VBA1
    vb3.name = "Car"
    vb3.balance = 400.00
    vb3.money_sub_month = 100
    vb3.icon = Icon.objects.filter(name="Car").first()
    vb3.save()

    vb3 = VirtualBankAccount.objects.create(bank_account = BankAccount.objects.get(account_number=2))     #BAcc2 VBA1
    vb3.name = "Food"
    vb3.balance = 400.00
    vb1.money_sub_month = 200
    vb3.icon = Icon.objects.filter(name="Food").first()
    vb3.save()

    vb4 = VirtualBankAccount.objects.create(bank_account = BankAccount.objects.get(account_number=3))     #BAcc3 VBA1
    vb4.name = "Car"
    vb4.balance = 15000.00
    vb1.money_sub_month = 400
    vb4.icon = Icon.objects.filter(name="Car").first()
    vb4.save()


    #Create Transaction
    print("Create Transactions")

    #client1 to client2
    Transaction.objects.all().delete()
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=1), virtual_bank = vb1) 
    t.recipient = "Hotel"
    t.description = "Holiday at Ibiza - 2361930"
    t.iban = "IT60 X222 2222 2220 0000 0222 222"
    t.bic = "RZSBIT21105"
    t.amount = 5.00
    t.is_assigned = False
    t.save()

    #client1 to client2
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=1), virtual_bank = vb2) 
    t.recipient = "Restaurant"
    t.description = "Bill 4296930-50305"
    t.iban = "IT60 X222 2222 2220 0000 0222 222"
    t.bic = "RZSBIT21105"
    t.amount = 50.00
    t.is_assigned = True
    t.save()

    #client2 to client1
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=2), virtual_bank = vb3)
    t.recipient = "Restaurant"
    t.description = "Bill 4296930-50305"
    t.iban = "IT60 X111 1111 1110 0000 0111 111"
    t.bic = "RZSBIT21007"
    t.amount = 600.00
    t.is_assigned = True
    t.save()

    #client2 to client3
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=2), virtual_bank = vb3)
    t.recipient = "Supermarket"
    t.description = "Return 2359303"
    t.iban = "IT60 X333 3333 3330 0000 0333 333"
    t.bic = "RZSBIT21007"
    t.amount = 20.00
    t.is_assigned = True
    t.save()

    #client3 to client1
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=3))
    t.recipient = "Programming Agency"
    t.description = "Salary 0438502 02348 02385"
    t.iban = "IT60 X111 1111 1110 0000 0111 111"
    t.bic = "RZSBIT21007"
    t.amount = 600.00
    t.is_assigned = False
    t.save()

    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=1), virtual_bank = vb1) 
    t.recipient = "Hotel"
    t.description = "Holiday at Ibiza - 2361930"
    t.iban = "IT60 X222 2222 2220 0000 0222 222"
    t.bic = "RZSBIT21105"
    t.amount = 5.00
    t.is_assigned = False
    t.save()

    #client1 to client2
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=1), virtual_bank = vb2) 
    t.recipient = "Restaurant"
    t.description = "Bill 4296930-50305"
    t.iban = "IT60 X222 2222 2220 0000 0222 222"
    t.bic = "RZSBIT21105"
    t.amount = 50.00
    t.is_assigned = True
    t.save()

    #client2 to client1
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=2), virtual_bank = vb3)
    t.recipient = "Restaurant"
    t.description = "Bill 4296930-50305"
    t.iban = "IT60 X111 1111 1110 0000 0111 111"
    t.bic = "RZSBIT21007"
    t.amount = 600.00
    t.is_assigned = True
    t.save()

    #client2 to client3
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=2), virtual_bank = vb3)
    t.recipient = "Supermarket"
    t.description = "Return 2359303"
    t.iban = "IT60 X333 3333 3330 0000 0333 333"
    t.bic = "RZSBIT21007"
    t.amount = 20.00
    t.is_assigned = True
    t.save()

    #client3 to client1
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=1))
    t.recipient = "Programming Course"
    t.description = "Transaction 235247-33432"
    t.iban = "IT60 X222 2222 2220 0000 0222 222"
    t.bic = "RZSBIT21007"
    t.amount = 50.00
    t.is_assigned = False
    t.save()

    #client2 to client1
    t = Transaction.objects.create(bank_account = BankAccount.objects.get(account_number=2))
    t.recipient = "Tutoring"
    t.description = "Summer Tutoring"
    t.iban = "IT60 X111 1111 1110 0000 0111 111"
    t.bic = "RZSBIT21007"
    t.amount = 100.00
    t.is_assigned = False
    t.save()



#Schmella Code Money Sharing

    #Create Sharing Group
    SharingGroup.objects.all().delete()
    sg = SharingGroup.objects.create(owner=User.objects.filter(username="client1").first())
    sg.name = "UniWG-Group"
    sg.save()

    sg = SharingGroup.objects.create(owner=User.objects.filter(username="client2").first())
    sg.name = "Vacation Money Sharing"
    sg.save()

    #Create SharingInfo
    SharingInfo.objects.all().delete()
    si = SharingInfo.objects.create(user=User.objects.filter(username="client1").first(),sharing_group=SharingGroup.objects.filter(name="UniWG-Group").first())
    si.balance = 0.0
    si.save()

    si = SharingInfo.objects.create(user=User.objects.filter(username="client2").first(),sharing_group=SharingGroup.objects.filter(name="UniWG-Group").first())
    si.balance = 0.0
    si.save()

    si = SharingInfo.objects.create(user=User.objects.filter(username="client3").first(),sharing_group=SharingGroup.objects.filter(name="UniWG-Group").first())
    si.balance = 0.0
    si.save()

    si = SharingInfo.objects.create(user=User.objects.filter(username="client2").first(),sharing_group=SharingGroup.objects.filter(name="Vacation Money Sharing").first())
    si.balance = 0.0
    si.save()

    si = SharingInfo.objects.create(user=User.objects.filter(username="client1").first(),sharing_group=SharingGroup.objects.filter(name="Vacation Money Sharing").first())
    si.balance = 0.0
    si.save()

    #Create Sharing Spenging
    SharingSpending.objects.all().delete()
    ss = SharingSpending.objects.create(sharing_group = SharingGroup.objects.filter(name="UniWG-Group").first(), paying_user=SharingInfo.objects.filter(user=User.objects.filter(username="client2").first()).first())
    ss.price = 50.0
    ss.description = "I bought groceries"
    ss.save()

    ss = SharingSpending.objects.create(sharing_group = SharingGroup.objects.filter(name="UniWG-Group").first(), paying_user=SharingInfo.objects.filter(user=User.objects.filter(username="client3").first()).first())
    ss.price = 20.0
    ss. description = "Beer Bill"
    ss.save()

    ss = SharingSpending.objects.create(sharing_group = SharingGroup.objects.filter(name="UniWG-Group").first(), paying_user=SharingInfo.objects.filter(user=User.objects.filter(username="client1").first()).first())
    ss.price = 80.0
    ss. description = "New Toaster"
    ss.save()
