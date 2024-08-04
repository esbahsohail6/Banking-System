from abc import ABC,abstractmethod
import datetime
import time

class account(ABC):
    """abstract class containing abstract method balance_enquiry"""
    def __init__(self,balance=0):
        self.balance=balance
    def withdraw(self,amount):
        self.balance-=amount
        print("your amount has been withdraw")
        time.sleep(1)
        return self.balance
    def deposit(self,amount):
        self.balance+=amount
        print("amount has been deposited")
        return self.balance
    @abstractmethod
    def balance_enquiry(self):
        pass


class checking_account(account):
    """allow user to deposit and withdraw the amount"""
    def __init__(self,balance=0,credit_limit=5000):
        super().__init__(balance)
        self.credit_limit=credit_limit
    def balance_enquiry(self):
        return self.balance
    def withdraw(self,amount):
        # overriding withdraw method
        if self.balance>amount<self.credit_limit:
            super().withdraw(amount)
        elif self.balance>amount>self.credit_limit or self.balance<amount>self.credit_limit:
            print("your amount has exceeded the credit limit")
            time.sleep(1)
        elif self.balance<amount<self.credit_limit:
            a = amount-self.balance
            print(f"your account does not have enough money\nOur bank will allow you overdraft,and the amount overdraft will be subtracted from your account later, that is {a}")
            time.sleep(1)
        return self.balance




class saving_account(account):
    """Facilitate user to safe balance with handsome interest"""
    def __init__(self,balance=0,interest_rate=20):
        super().__init__(balance)
        self.interest_rate=interest_rate
    def balance_enquiry(self):
        return self.balance
    def monthly_interest(self):
        # calculates monthly interest on total balance
        self.balance_interest=self.balance*(self.interest_rate/100)
        self.balance+=self.balance_interest
        print(f"your balance is incremented to {self.balance}")
        time.sleep(1)
        return self.balance



class loan_account(account):
    """Allows user to take loan from the bank"""
    def __init__(self,balance,principal_amount=0,loan_duration=0,interest_rate=20,monthly_payment=0):
        super().__init__(balance)
        self.principal_amount=principal_amount
        self.loan_duration=loan_duration
        self.interest_rate=interest_rate
        self.monthly_payment=monthly_payment
    def balance_enquiry(self):
        return self.balance
    def loan_payement(self):
        self.monthly_payment=(self.principal_amount*self.interest_rate)/(1-1/(1+self.interest_rate)**(self.loan_duration))
        # calculates monthly payment on the total balance
        total_payment=self.monthly_payment*self.loan_duration
        print(f"your total loan payment with interest is {total_payment}\nyour monthly loan payement is {self.monthly_payment}")
        time.sleep(1)
        return self.balance


class customer:
    """takes basic information from the user to kepp record"""
    def __init__(self, username, password, first_name, last_name, address,balance=0):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.balance=balance
        self.accounts={}



    def create_account(self,account_type,balance=0):
        """creates new account for the user"""
        if account_type=="checking" or account_type=="saving" or account_type =="loan":
            #if true it will return 0
            print("account created successfully")
            time.sleep(1)
            self.accounts["Name"] = self.username
            self.accounts["password"] = self.password
            self.accounts["first_name"] = self.first_name
            self.accounts["last_name"] = self.last_name
            return 0
        else:
            print("Invalid account type.")
            time.sleep(1)
            return 1



    def login_account(self,username,password,first_name,last_name):
        """Allows user to login to the account"""
        self.accounts["Name"] = self.username
        self.accounts["password"] = self.password
        self.accounts["first_name"] = self.first_name
        self.accounts["last_name"] = self.last_name
        # opening file in append + mode
        f=open("customer_details.txt","a+")
        f.seek(0)
        for line in f:
            line=eval(line)
            if line["Name"]==username and line["password"]==password:
                # updating balance
                self.balance=line["current_balances"]
                # self.accounts["current_balance"]=self.balance
                return True

class banking_system:
    """provide our software with interface"""
    def __init__(self,username,password,first_name,last_name,address):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.info={}

    def transaction_history(self):
        f2=open("transactions.txt","r")
        #  opening transaction file in read mode
        choice=input("enter y to print transaction: ")
        if choice=="y":
            for line in f2:
                line = eval(line)
                if line["first-name"] == self.first_name and line["last_name"] == self.last_name:
                    print(line)
        else:
            pass

    def criteria(self,choice1,interest_rate=20):
        if choice1==1:
            # making the object of customer class in banking_system
            a=customer(self.username,self.password,self.first_name,self.last_name,self.address)
            # 1 for signin and 2 for login
            option=int(input("press 1 to create account and 2 for login account:"))
            time.sleep(1)
            self.info["first-name"] = self.first_name
            self.info["last_name"] = self.last_name

            if option==1:
                # taking balance input
                balance=int(input("enter your initial balance:"))
                time.sleep(1)
                account_type = input("checking,saving or loan:")
                time.sleep(1)
                self.info["account_type"] = account_type
                if a.create_account(account_type,balance)==0:
                    current_balance=0
                    if account_type == "checking":
                        # calling checking class
                        account2 = checking_account(balance)
                        choice2 = int(input("press 1 to deposit and 2 to withdraw: "))
                        time.sleep(1)
                        amount = int(input("enter amount:"))
                        time.sleep(1)
                        if choice2 == 1:
                            # setting keys to transaction and amount
                            self.info["transaction"] = "deposit"
                            self.info["amount"] = amount
                            # updating balance
                            current_balance+=account2.deposit(amount)
                        elif choice2 == 2:
                            # setting values to transaction and amount
                            self.info["transaction"] = "withdraw"
                            self.info["amount"] = amount
                            # updating balance
                            current_balance+=account2.withdraw(amount)
                    elif account_type == "saving":
                        # calling saving class
                        account2 = saving_account(balance)
                        current_balance+=account2.monthly_interest()
                        self.info["monthly interest"] = account2.balance_interest
                    elif account_type == "loan":
                        # calling loan class
                        principal_amount = int(input("enter your principal amount: "))
                        loan_duration = int(input("enter loan duration in months"))
                        account2 = loan_account(balance, principal_amount, loan_duration, interest_rate)
                        current_balance+=account2.loan_payement()
                        self.info["monthly loan payment"] = account2.monthly_payment
                    # keeping record of the date and time when the account is signing in
                    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.info["date_time"] = date_time
                    a.accounts["current_balances"] = current_balance
                    f2 = open("transactions.txt", "a+")
                    # writing info to the transaction file
                    f2.write(f"{self.info}\n")
                    f2.close()
                    f = open("customer_details.txt", "a+")
                    # writing info to the customer_details file
                    f.write(f"{a.accounts}\n")
                    f.close()
                    self.transaction_history()
                else:
                    pass


            elif option==2:
                # calling login method of customer account
                if a.login_account(self.username, self.password,first_name,last_name)==True:
                    balance=a.balance
                    print("account logged in successfully")
                    time.sleep(1)
                    account_type = input("checking,saving or loan:")
                    self.info["account_type"] = account_type
                    current_balance=0
                    if account_type == "checking":
                        account2 = checking_account(balance)
                        # calling checking class
                        choice2 = int(input("press 1 to deposit and any key to withdraw: "))
                        time.sleep(1)
                        amount = int(input("enter amount:"))
                        # taking the amount input to withdraw or deposit from the balance
                        time.sleep(1)
                        if choice2==1:
                            self.info["transaction"] = "deposit"
                            self.info["amount"] = amount
                            # calling deposit method
                            self.current_balance=account2.deposit(amount)
                        elif choice2==2:
                            self.info["transaction"] = "withdraw"
                            self.info["amount"] = amount
                            # calling withdraw method
                            self.current_balance=account2.withdraw(amount)
                    elif account_type == "saving":
                        account2 = saving_account(balance)
                        self.current_balance=account2.monthly_interest()
                        # setting value to monthly interest
                        self.info["monthly interest"] = account2.balance_interest
                    elif account_type == "loan":
                        # calling loan account
                        principal_amount = int(input("enter your principal amount: "))
                        time.sleep(1)
                        # taking loan duration as input
                        loan_duration = int(input("enter loan duration in months"))
                        time.sleep(1)
                        account2 = loan_account(balance, principal_amount, loan_duration, interest_rate)
                        self.current_balance=account2.loan_payement()
                        self.info["monthly loan payment"] = account2.monthly_payment
                    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.info["date_time"] = date_time
                    # opening transaction in append mode
                    f2 = open("transactions.txt", "a+")
                    # writing info to the transaction file
                    f2.write(f"{self.info}\n")
                    f2.close()
                    # opening customer_details in read mode
                    f = open("customer_details.txt", "r+")
                    f.seek(0)
                    d=[]
                    for line in f:
                        d.append(line)
                    f3=open("customer_details.txt","w")
                    for i in d:
                        i=eval(i)
                        if i["Name"]==self.username and i["password"]==self.password:
                            # updating balance
                            i["current_balances"]=self.current_balance
                        f3.write(f"{i}\n")
                    f3.close()

                    # File path
                    # calling transaction
                    self.transaction_history()
                else:
                    print("invalid password")
                    time.sleep(1)
        elif choice1==2:
            # admin mode has access to all the files
            choice3=int(input("enter 1 to reset file and 2 to access data of the file"))
            time.sleep(1)
            if choice3==1:
                f=open("customer_details.txt","w")
            elif choice3==2:
                f=open("customer_details.txt","r")
                print(f.read())
        else:
            print("invalid input")
            time.sleep(1)
print("*****Welcome to our Bank*****")
username = input("enter your name: ")
password = input("enter your password: ")
first_name = input("enter your first name: ")
last_name = input("enter your last name: ")
address = input("enter your address: ")
while True:
    try:
        choice = int(input("enter 1 to continue and 2 to exit: "))
    except ValueError:
        print('enter valid input')
    if choice == 1:
        bank = banking_system(username, password, first_name, last_name, address)
        choice1 = int(input("enter 1 for customer and 2 for admin mode"))
        bank.criteria(choice1)
    else:
        print("THANK YOU FOR VISITING")
        break





















#


