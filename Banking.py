import csv
import os

CSV_FILE = "bank.csv"


####################################
class Account:
    OVERDRAFT_LIMIT = -100
    OVERDRAFT_FEE = 35
    MAX_WITHDRAW = 100
#########
    def __init__(self, customer_id, account_kind, balance=0):
        self.customer_id = customer_id 
        self.account_kind = account_kind
        self.balance = float(balance)
        self.overdraft_count = 0 
        self.active = True  
#########
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("The deposited amount must be greater then zero")
        self.balance += amount
        
        if self.balance >= 0:
            self.active = True
            self.overdraft_count = 0
        return self.balance
    
#########
    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("The withdrawn amount must be greater then zero")
        if amount > Account.MAX_WITHDRAW:
            raise ValueError(f"You cannot withdraw more then {Account.MAX_WITHDRAW}")

        new_balance = self.balance - amount
        if new_balance < Account.OVERDRAFT_LIMIT:
            raise ValueError("The balance cannot fall below -100")

        self.balance = new_balance

        if self.balance < 0:
            self.balance -= Account.OVERDRAFT_FEE
            self.overdraft_count += 1
            if self.overdraft_count >=2:
                self.active = False
                raise ValueError("Account deactivated after 2 overdrafts")

        return self.balance

    def __str__(self):
        return f"{self.account_kind} Account | Balance: {self.balance}"

###################################


class Savings(Account):
    def __init__(self, customer_id, balance=0):  
        super().__init__(customer_id, "savings", balance)


class Checking(Account):
    def __init__(self, customer_id, balance=0):
        super().__init__(customer_id, "checking", balance)


####################################
class Customer:
    def __init__(self,customer_id,first_name,last_name,password,checking_balance=None,savings_balance=None,):
        self.customer_id = customer_id.strip()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.password = password.strip()
        self.accounts = {}
        self.is_logged_in = False

        if checking_balance is not None:
            self.accounts["checking"] = Checking(customer_id, checking_balance)

        if savings_balance is not None:
            self.accounts["savings"] = Savings(customer_id, savings_balance)

########
    def add_account(self, account_kind, balance=None):
        Mb = account_kind.strip().lower()
        if Mb in self.accounts:
            raise ValueError(f"You already have {account_kind} account")

        if Mb == "savings":
            acco = Savings(self.customer_id, balance) 
        elif Mb == "checking":
            acco = Checking(self.customer_id, balance)  
        else:
            raise ValueError("Unknown account")
        self.accounts[Mb] = acco
        return acco
##########
    def get_account(self, account_kind):
        return self.accounts.get(account_kind.lower())

####### تسجيل دخول
    def login(self, customer_id, password): 
        if customer_id == self.customer_id and password == self.password:
            self.is_logged_in = True
            print(f"{self.first_name} logged in successfully!")
            return True
        else:
            print("Invalid ID or password.")
            return False

#####تسجيل خروج
    def logout(self):
        if self.is_logged_in:
            self.is_logged_in = False
            print(f"{self.first_name} logged out.")

        else:
            print("You are not logged in .")

#########
    def transfer(self, from_acc, to_acc, amount, target_customer=None):
        src = self.get_account(from_acc)
        if target_customer:
            com = target_customer.get_account(to_acc)
        else:
            com = self.get_account(to_acc)

        if not src or not com:
            print("Invalid accounts")
            return False
        
        if not src.active:
            print(f"{from_acc.capitalize()} account is inactive.")
            return False
        
        if not com.active:
            print(f"{to_acc.capitalize()} account is inactive.")
            return False
            
        try:
            src.withdraw(amount)
            com.deposit(amount)
            print(f"Transferred ${amount} from {from_acc} to {to_acc}")
            return True
        except ValueError as error:
            print(f"Transfer failed:{error}")
            return False
        
###########################################
class Bank_repo:
    def __init__(self):
        self.customers = []
#########
    def add_customer(self, customer):

        print("welcome! Do you want to open an account? (Yes/No)")
        choice = input().strip().lower()

        if choice == "yes":
            Account_kind = input(
                "which type of account do you want? (Savings/Checking):"
            ).strip().lower()
            try:
                initial_balance= float(input("Enter initial balance for the account: "))
                customer.add_account(Account_kind, initial_balance)## ضفت قيمه بدائيه
                print(f"{Account_kind.capitalize()} account created for {customer.first_name}"
                )

            except ValueError as error_msg:
                print(f"{error_msg}")
        else:
            print("Customer registered without an account.")

        self.customers.append(customer)
        print(f"Customer'{customer.first_name}' added successfully!")
##########
    def load_customers(self): 
        self.customers = []
        try:
            with open(CSV_FILE, newline="") as file:
                #print(file.read())
                contents = csv.DictReader(file)
                for row in contents:
                    if row["checking"] == "False":
                        checking = False
                    else :
                        checking = float(row["checking"]) if row["checking"] else 0
                    
                    if row["savings"] == "False":
                        savings = False
                    else:
                        savings = float(row["savings"]) if row["savings"] else 0
                    cust1 = Customer(
                        customer_id=row["id"].strip(),
                        
                        first_name=row["first_name"].strip(),
                        last_name=row["last_name"].strip(),
                        password=row["password"].strip(),
                        checking_balance=checking,
                        savings_balance=savings,
                    )

                    checking_acc = cust1.get_account("checking")
                    if checking_acc:
                        if row.get("checking_active"):
                            checking_acc.active = row["checking_active"].lower() == "true"
                        if row.get("checking_overdraft"):
                            checking_acc.overdraft_count = int(row["checking_overdraft"])

                    savings_acc = cust1.get_account("savings")
                    if savings_acc:
                        if row.get("savings_active"):
                            savings_acc.active = row["savings_active"].lower() == "true"
                        if row.get("savings_overdraft"):
                            savings_acc.overdraft_count = int(row["savings_overdraft"])

                    self.customers.append(cust1)

            print("Loaded customers:", [c.customer_id for c in self.customers])

        except FileNotFoundError:
            print("File not found. Starting with empty customer list.")
            # print("\nLoaded customers:")
            # print("{:<8} {:<12} {:<12} {:<12} {:<10} {:<10}".format(
            #     "ID", "First Name", "Last Name", "Password", "Checking", "Savings"
            # ))
            # print("-" * 70)
            # for c in self.customers:
            #     checking = c.accounts["checking"].balance if "checking" in c.accounts else 0
            #     savings = c.accounts["savings"].balance if "savings" in c.accounts else 0
            #     print("{:<8} {:<12} {:<12} {:<12} {:<10} {:<10}".format(
            #         c.customer_id, c.first_name, c.last_name, c.password, checking, savings
            #     ))

                    
               
#######
    def find_customer(self, customer_id):
     return next((c for c in self.customers if c.customer_id == customer_id), None)
#######
    def save_to_csv(self):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
    ["id","first_name","last_name","password","checking","savings","active","overdraft_count"
]

)
            for cust in self.customers:
                checking = cust.accounts.get("checking")
                savings = cust.accounts.get("savings")
                writer.writerow(
                    [
                        cust.customer_id,
                        cust.first_name,
                        cust.last_name,
                        cust.password,
                        checking.balance if checking else "",
                        checking.active if checking else "",
                        checking.overdraft_count if checking else "",
                        savings.balance if savings else "",
                        savings.active if savings else "",
                        savings.overdraft_count if savings else "",
                    ])
#########
def main():
    bank = Bank_repo()
    bank.load_customers()
    current_user = None

    print("=== ** Welcome to Bank 🏦 ** ===")

    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Create new customer")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. View accounts")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            customer_id = input("Enter your ID: ").strip()
            password = input("Enter your password: ").strip()
            cust = bank.find_customer(customer_id)
            if cust and cust.login(customer_id, password):
                current_user = cust
                print(f"{cust.first_name} logged in successfully!")
            else:
                print("Login failed: wrong ID or password.")

        elif choice == "2":
            customer_id = input("Enter new customer ID: ").strip()
            first_name = input("Enter first name: ").strip()
            last_name = input("Enter last name: ").strip()
            password = input("Enter password: ").strip()
            cust = Customer(customer_id, first_name, last_name, password)
            bank.add_customer(cust)

        elif choice == "3":
            if current_user:
                acc_type = input("Which account? (checking/savings): ").lower()
                amount = float(input("Amount to deposit: "))
                acc = current_user.get_account(acc_type)
                if acc:
                    acc.deposit(amount)
                    print(f"${amount} deposited to {acc_type}.")
                else:
                    print("Account not found.")
            else:
                print("Login first.")

        elif choice == "4":
            if current_user:
                acc_type = input("Which account? (checking/savings): ").lower()
                amount = float(input("Amount to withdraw: "))
                acc = current_user.get_account(acc_type)
                if acc:
                    try:
                        acc.withdraw(amount)
                        print(f"${amount} withdrawn from {acc_type}.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Account not found.")
            else:
                print("Login first.")

        elif choice == "5":
            if current_user:
                from_acc = input("From account? (checking/savings): ").lower()
                to_acc = input("To account? (checking/savings): ").lower()
                amount = float(input("Amount to transfer: "))
                target_id = input("Target customer ID (Enter for own account): ").strip()
                target_cust = bank.find_customer(target_id) if target_id else None
                current_user.transfer(from_acc, to_acc, amount, target_customer=target_cust)
            else:
                print("Login first.")

        elif choice == "6":
            if current_user:
                for acc_name, acc in current_user.accounts.items():
                    print(acc)
            else:
                print("Login first.")

        elif choice == "7":
            bank.save_to_csv()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
###################################