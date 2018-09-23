from .open_hub import OpenHub
from .models import *

class KiliansIndex:


    def get_connection():
        OH=OpenHub()
        OH.connect()
        return OH

    def apply(oh,t,user):
        json=oh.get_gastronomy_reduced()
        for g in json:
            val=g['Name']
            if(val==None):
                    continue
            val=val.lower()
            if(val in t.description.lower() or val in t.recipient.lower()):
                icon=Icon.objects.get(name="Food")
                vba=VirtualBankAccount.objects.all().filter(bank_account__owner=user,icon=icon)
                vba=vba[0]
                t.virtual_bank=vba
                t.is_assigned=True
                t.save()
                if(t.is_outgoing(user)):
                    TagIndex.make(user,t.iban,vba.icon)
                return True
        return False

