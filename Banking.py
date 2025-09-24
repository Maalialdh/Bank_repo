import csv
import os

CSV_FILE = "bank.csv"


####################################
class Account:
    OVERDRAFT_LIMIT = -100
    OVERDRAFT_FEE = 35
    MAX_WITHDRAW = 100

    def __init__(self, customer_id, account_kind, balance=0):
        self.customer_id = customer_id  # عشان اتتبع حساب لكل عميل
        self.account_kind = account_kind
        self.balance = float(balance)
        self.overdraft_count = 0  # اضافه جديده
        self.active = True  # اضافه جديدهه

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("The deposited amount must be greater then zero")
        self.balance += amount
        return self.balance

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
            if self.overdraft_count > 2:
                self.active = False
                raise ValueError("Account deactivated after 2 overdrafts")

        return self.balance

    ###### هنا فيه تعديل
    def __str__(self):
        return f"{self.account_kind} Account | Balance: {self.balance}"


###################################
###################################
###################################


class Savings(Account):
    def __init__(self, customer_id, balance=0):  # حذفتتتت النوع
        super().__init__(customer_id, "savings", balance)


#####################################


class Checking(Account):
    def __init__(self, customer_id, balance=0):  # حذفت النوع
        super().__init__(customer_id, "checking", balance)


####################################
####################################
class Customer:
    def __init__(self,customer_id,first_name,last_name,password,checking_balance=None,savings_balance=None,
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.accounts = {}
        self.is_logged_in = False

        if checking_balance is not None:
            self.accounts["checking"] = Checking(customer_id, checking_balance)

        if savings_balance is not None:
            self.accounts["savings"] = Savings(customer_id, savings_balance)

    #####################################################
    def add_account(self, account_kind, balance=None):
        Mb = account_kind.lower()
        if Mb in self.accounts:
            raise ValueError(f"You already have {account_kind} account")

        if Mb == "savings":
            acco = Savings(self.customer_id, balance)  # account_kind حذفتها
        elif Mb == "checking":
            acco = Checking(self.customer_id, balance)  # account_kind حذفتها
        else:
            raise ValueError("Unknown account")
        self.accounts[Mb] = acco
        return acco

    def get_account(self, account_kind):
        return self.accounts.get(account_kind.lower())

    #####################
    ############ تسجيل دخول
    def login(self, customer_id, password):
        # customer_id=input("enter your id :")
        # password=input("enter your password: ")
        if customer_id == self.customer_id and password == self.password:
            self.is_logged_in = True
            print(f"{self.first_name} Logged in successful!")
            return True
        print("Invalid id or password.")
        return False

    ######################################
    #####تسجيل خروج
    def logout(self):
        if self.is_logged_in:
            self.is_logged_in = False
            print(f"{self.first_name} logged out.")

        else:
            print("You are not logged in .")

    ###########################
    def transfer(self, from_acc, to_acc, amount, target_customer=None):
        src = self.get_account(from_acc)
        if target_customer:
            com = target_customer.get_account(to_acc)
        else:
            com = self.get_account(to_acc)

        if not src or not com:
            print("Invalid accounts")
            return False

        try:
            src.withdraw(amount)

            com.deposit(amount)
            print(f"Transferrd ${amount} from {from_acc}to{to_acc}")
            return True
        except ValueError as error:
            print(f"Transfer failed:{error}")
            return False


###########################################
###########################################
###########################################


class Bank_repo:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):

        print("welcome! Do you want to open an account? (Yes/No)")
        choice = input().lower()

        if choice == "yes":
            Account_kind = input(
                "which type of account do you want? (Savings/Checking):"
            ).lower()
            try:
                customer.add_account(Account_kind)
                print(
                    f"{Account_kind.capitalize()} account created for {customer.first_name}"
                )

            except ValueError as error_msg:
                print(f"{error_msg}")
        else:
            print("Customer registered without an account.")

        self.customers.append(customer)
        print(f"Customer'{customer.first_name}' added successfully!")

    def add_all_customer(self):
        try:
            with open(CSV_FILE, "r") as file:
                contents = csv.DictReader(file)
                for row in contents:
                    cust1 = Customer(
                        customer_id=row["id"],
                        last_name=row["last_name"],
                        first_name=row["first_name"],
                        password=row["password"],
                        checking_balance=int(row["checking"]),
                        savings_balance=int(row["savings"]),
                        # ضفت 2 الاخيرات
                    )
                    self.customers.append(cust1)
        except csv.Error as error_msg:
            print("CSV Error:", error_msg)
        except KeyError as error_msg:
            print("Missing column in CSV:", error_msg)

    ############################################ "يبيلها تعديل"
    def save_to_csv(self):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["id", "first_name", "last_name", "password", "checking", "savings"]
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
                        savings.balance if savings else "",
                    ]
                )


#####################################################
####################################
####################################
# se;f.customers that contains the customers that already exist in the bank

# method that adds customer to this self.customers
# username = input("Enter username: ")
#  password = input("Enter password: ")
# new_customer = Customer(username, password)
# create an instance pf the class Bank
# ex = Bank_repo()
# cust1 = Customer("Ali", 1233)
# ex.add_customer(cust1)
# example for creating a customer --> cust1  = Customer (username, password)
# vreate a customer and add it to the bank


# check that the bank has a new customer, by printing the value of customers in the instance of bank
# add an account to customer
