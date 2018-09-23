from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class BankAccount(models.Model):
    account_number = models.IntegerField(default=0)
    balance = models.FloatField(default=0.0)
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    iban = models.CharField(max_length=255)
    bic = models.CharField(max_length=255)
    money_sub_month = models.FloatField(default=0.0)
    money_in_last_month = models.FloatField(default=2500.0)
    money_out_last_month = models.FloatField(default=1000.0)
    
    def icon(self):
        return Icon.objects.all().filter(name="Default").first()

    def sub_money_from_default_virtual_account(self, amount):
        self.money_sub_month = self.money_sub_month + amount
        self.balance = self.balance - amount
        self.save()
        

    def get_balance(self):
        vbas=VirtualBankAccount.objects.all().filter(bank_account=self)
        b = self.balance;
        for v in vbas:
            b = b - v.balance
        return b

    def add_money(self, amount):
        self.balance= self.balance + amount
        self.save()

    def calc_fpm_percentage(self):
        return self.money_sub_month / 1500 * 100

    def calc_fpm_percentage_max_100(self):
        return min(self.money_sub_month / 1500 * 100,100)

    def color_from_percentage(self):
        z=self.calc_fpm_percentage_max_100()
        if(z<60):
            return '#0ba070'
        return '#e23c3c'

class Icon(models.Model):
    name = models.CharField(max_length=255, blank = True, null = True)
    icon = models.CharField(max_length=255, blank=False, null=False)
    avg_output =models.FloatField(default=0.0)

    def __str__(self):
        return self.icon

class VirtualBankAccount(models.Model):
    name = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccount, null=False, blank=False, on_delete=models.CASCADE)
    icon = models.ForeignKey(Icon, blank=False, null=True, on_delete=models.SET_NULL)
    balance = models.FloatField(default=0.0)
    percentage_of_amount = models.FloatField(default=0.0,blank=True, null=True)

    money_added_month = models.FloatField(default=0.0)
    money_sub_month = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    

    def get_by_user(user):
        ba = BankAccount.objects.get(owner=user)
        return VirtualBankAccount.objects.all().filter(bank_account=ba)

    def add_money(self, amount,complete=True):
        self.money_added_month = self.money_added_month + amount
        self.balance = self.balance + amount
        if(complete):
            self.bank_account.add_money(amount)
        self.save()

    def sub_money(self, amount,complete=True):
        self.money_sub_month = self.money_sub_month + amount
        self.balance = self.balance - amount
        if(complete):
            self.bank_account.add_money(-amount)
        self.save()

    def move_money_to_default(self,amount):
        amount=-amount
        if(amount<0):
            if(self.balance<-amount):
                amount=-self.balance
        else:
            if(self.bank_account.get_balance()<amount):
                amount=self.bank_account.get_balance()
        self.balance = self.balance + amount
        self.save()

    def calc_fpm_percentage(self):
        return self.money_sub_month / self.icon.avg_output * 100 -100

    def calc_fpm_percentage_max_100(self):
        return min(self.money_sub_month / self.icon.avg_output * 50,100)

    def color_from_percentage(self):
        z=self.calc_fpm_percentage_max_100()
        if(z<60):
            return '#0ba070'
        return '#e23c3c'
        


class Transaction(models.Model):
    virtual_bank = models.ForeignKey(VirtualBankAccount, on_delete=models.SET_NULL, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True)

    recipient = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    iban = models.CharField(max_length=255, blank=False, null=False)
    bic = models.CharField(max_length=255, blank=False, null=False)
    amount = models.FloatField(default=0.0, blank=False, null=False)
    is_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,null=True)
    updated_at = models.DateTimeField(auto_now=True,editable=False,null=True)

    def get_unassigned_by_user(user):
        return Transaction.objects.filter(bank_account__owner=user, is_assigned=False)

    def is_incomming(self,current_user):
        user_iban = BankAccount.objects.all().filter(owner=current_user).first().iban
        return self.iban == user_iban
    
    def is_outgoing(self,current_user):
        return not self.is_incomming(current_user)


    class Meta:
        ordering = ['-created_at']
        
    def get_by_user(user):
        return Transaction.objects.filter(bank_account__owner=user)

    def get_by_recipient(user):
        ba=BankAccount.objects.get(owner=user)
        return Transaction.objects.filter(iban=ba.iban)

class TagIndex(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    iban = models.CharField(max_length=255, blank=False, null=False)
    icon = models.ForeignKey(Icon, blank=False, null=True, on_delete=models.CASCADE)

    def make(user,iban,icon):
        t=TagIndex(user=user,iban=iban,icon=icon)
        q=TagIndex.objects.filter(iban=iban)
        if(q):
            t.pk=q[0].pk
        t.save()

    def getIcon(u, i):
        q=TagIndex.objects.filter(user=u,iban=i).first()
        if(q):
            return q.icon
        else:
            return None

    class Meta:
        unique_together = (('iban','user'),)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (("can_delete_user", "Delete User"),("can_create_user", "Create User"),("can_edit_user", "Edit User"))
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




#Schmella Code Money Sharing

class SharingGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, blank = True, null = True)

class SharingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sharing_group = models.ForeignKey(SharingGroup, on_delete=models.CASCADE, null =True)
    sharing_balance = models.FloatField(default=0.0, blank=False, null=False)


class SharingSpending(models.Model):
    sharing_group = models.ForeignKey(SharingGroup, on_delete=models.SET_NULL, null=True)
    paying_user = models.ForeignKey(SharingInfo, on_delete=models.SET_NULL, null=True)

    price = models.FloatField(default=0.0, blank=False, null=False)
    description = models.CharField(max_length=255, blank = True, null = True)
    
    def calc_balance(group):
        l=[]
        people=SharingInfo.objects.all().filter(sharing_group=group)
        for p in people:
            ss=SharingSpending.objects.all().filter(paying_user=p)
            sum=0
            for s in ss:
                sum=sum+s.price
            l.append((p.user,sum))
        return l #[(u1,34),(u2,214),...]
            

    def get_triple(group):
        l=SharingSpending.calc_balance(group)
        sum=0
        for i in l:
            sum=sum+i[1]
        avg=sum/len(l)
        l2=[]
        l_users=[]
        l_sum=[]
        for p in l:
            l2.append((p[0],p[1]-avg)) #p1 = User, p2= abweichung von Average +/-
            l_users.append(p[0])
            l_sum.append(p[1]-avg)
        return l_users,l_sum, avg       #returns list of users and list of pay values of users(=abweichung von Average +/-) and avg
            


    def transaction(group):
        l_users,l_sum, avg = SharingSpending.get_triple(group)      #l=liste von calc _balance
        highest=max(l_sum)
        max_index = l_sum.index(max(l_sum))
        lowest=min(l_sum)
        min_index = l_sum.index(min(l_sum))
        while(True):
            if(highest == avg or lowest == avg):
                #no transaction... look if all sums are the same as avg
                if(highest==avg and lowest==avg):
                    break
                elif(highest != avg or lowest != avg):
                    print("Error - Payments can not be authorized")
            elif(highest + lowest > avg):
                #user at lowest index pays user at highest index
                user_pay = l_users[min_index]
                user_recieve = l_users[max_index]
                payment = -lowest

                l_sum[min_index] = lowest + payment
                l_sum[max_index] = highest - payment
                if(l_sum[min_index]!= avg or l_sum[max_index]!=avg):
                    print("Error - Transaction error")
                    break
                    #cancel Transaction

                #TRANSACTION
                make_transaction(user_pay, user_recieve,payment,"Money Sharing","RZSBIT21105")
            
            elif(highest + lowest < avg):
                user_pay = l_users[min_index]
                user_recieve = l_users[max_index]
                payment = highest - avg
                #balance in list gets updated -> lowest gets paysum added and highest gets paysum substracted
                l_sum[min_index] = lowest + payment
                l_sum[max_index] = highest - payment
                #user at lowest index pays user at highest index the paysum
                if(l_sum[min_index]!= avg or l_sum[max_index]!=avg):
                    print("Error - Transaction error")
                    break
                    #cancel Transaction

                #TRANSACTION
                make_transaction(user_pay, user_recieve,payment,"Money Sharing","RZSBIT21105")
            
    def make_transaction(sender,reciver,amount,desc="Money Sharing", bic="RZSBIT21105"):
        Transaction.objects.create(bank_account=BankAccount.objects.get(owner=sender),recipient=reciver.lastname,descriptio=desc,iban=BankAccount.objects.get(owner=reciver).iban,bic=bic,amount=amount)
        
