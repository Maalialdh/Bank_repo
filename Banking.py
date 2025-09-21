import csv

class Customer:
    def __init__(self,username,Pasword,customer_id=None):
        self.username=username
        self.Pasword=Pasword
        self.customer_id=customer_id
        self.accounts={} 
    def add_account(self,account_kind):
        if account_kind in self.accounts:
            raise ValueError(f"You have already Account{account_kind}")
        acct=account(self,customer_id,account_kind)
        self.accounts[account_kind]





#_______________________________________________
