from datetime import datetime

AGENCY_NUMBER = "001"
TRANSACTION_LIMIT = 10
WITHDRAW_LIMIT = 500

def format_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

class Account:
    def __init__(self, account_number):
        self.account_number = account_number
        self.balance = 0
        self.statement = ""
        self.transactions = 0

    def deposit(self, value):
        if self.transactions >= TRANSACTION_LIMIT:
            print("You exceeded the transaction limit!")
            return

        if value > 0:
            self.balance += value
            transaction_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            self.statement += f"Deposit: R$ {value:.2f} at {transaction_time} \n"
            self.transactions += 1
            print(f"Successfully deposited R$ {value:.2f}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, value):
        if self.transactions >= TRANSACTION_LIMIT:
            print("You have exceeded the transaction limit.")
            return

        if value > self.balance:
            print("Operation failed! You don't have enough balance.")
        elif value > WITHDRAW_LIMIT:
            print("Operation failed! You have exceeded the withdrawal limit.")
        elif value > 0:
            self.balance -= value
            transaction_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            self.statement += f"Withdraw: R$ {value:.2f} at {transaction_time}\n"
            self.transactions += 1
            print(f"Successfully withdrew R$ {value:.2f}")
        else:
            print("Invalid withdrawal amount.")

    def show_statement(self):
        print("\n====== Statement ======\n")
        print("No transactions were made." if not self.statement else self.statement)
        print(f"\nBalance: R$ {self.balance:.2f}")
        print("\n=======================")


class User:
    def __init__(self, name, dob, cpf, address):
        self.name = name
        self.dob = dob
        self.cpf = cpf
        self.address = address
        self.accounts = {}

    def create_account(self):
        account_number = f"{AGENCY_NUMBER}-{len(self.accounts) + 1:04d}"
        self.accounts[account_number] = Account(account_number)
        return account_number

    def display_user_info(self):
        formatted_cpf = format_cpf(self.cpf)
        print(f"Name: {self.name}")
        print(f"Date of Birth: {self.dob}")
        print(f"CPF: {formatted_cpf}")
        print(f"Address: {self.address}")

    def list_accounts(self):
        if not self.accounts:
            print("No accounts found for this user.")
        else:
            print(f"User: {self.name}")
            for account_number in self.accounts:
                print(f"Account Number: {account_number}, Agency: {AGENCY_NUMBER}")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

class Agency:
    def __init__(self, agency_number):
        self.agency_number = agency_number
        self.users = {}

    def create_user(self, name, dob, cpf, address):
        if cpf in self.users:
            print("User with this CPF already exists.")
            return self.users[cpf]

        user = User(name, dob, cpf, address)
        self.users[cpf] = user
        print(f"User {name} created successfully.")
        return user

    def get_user(self, cpf):
        return self.users.get(cpf)


class BankSystem:
    def __init__(self):
        self.agency = Agency(AGENCY_NUMBER)

    def display_menu(self):
        print("""
              
[D] -> Deposit
[W] -> Withdraw
[S] -> Statement
[E] -> Exit
[C] -> Create Account
[A] -> Create User
[L] -> List Accounts
              
""")

    def main(self):
        while True:
            self.display_menu()
            option = input().strip().upper()

            if option == 'D':
                self.handle_deposit()
            elif option == 'W':
                self.handle_withdraw()
            elif option == 'S':
                self.handle_statement()
            elif option == 'C':
                self.handle_create_account()
            elif option == 'A':
                self.handle_create_user()
            elif option == 'L':
                self.handle_list_accounts()
            elif option == 'E':
                break
            else:
                print("Invalid operation, please enter a valid option.")

    def handle_deposit(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            account_number = input("Enter your account number: ")
            account = user.get_account(account_number)
            if account:
                value = float(input("Enter the deposit amount: "))
                account.deposit(value)
            else:
                print("Account not found.")
        else:
            print("User not found.")

    def handle_withdraw(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            account_number = input("Enter your account number: ")
            account = user.get_account(account_number)
            if account:
                value = float(input("Enter the amount you want to withdraw: "))
                account.withdraw(value)
            else:
                print("Account not found.")
        else:
            print("User not found.")

    def handle_statement(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            account_number = input("Enter your account number: ")
            account = user.get_account(account_number)
            if account:
                account.show_statement()
            else:
                print("Account not found.")
        else:
            print("User not found.")

    def handle_create_account(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            account_number = user.create_account()
            print(f"Account created successfully! Your account number is {account_number}")
        else:
            print("User not found.")

    def handle_create_user(self):
        name = input("Enter your name: ")
        dob = input("Enter your date of birth (dd-mm-yyyy): ")
        cpf = input("Enter your CPF (only numbers): ")
        address = input("Enter your address (logradouro, número, bairro, cidade/sigla e estado): ")
        user = self.agency.create_user(name, dob, cpf, address)
        if user:
            account_number = user.create_account()
            print(f"User and account created successfully! Your account number is {account_number}")

    def handle_show_user_info(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            user.display_user_info()
        else:
            print("User not found.")

    def handle_list_accounts(self):
        cpf = input("Enter your CPF: ")
        user = self.agency.get_user(cpf)
        if user:
            user.list_accounts()
        else:
            print("User not found.")     


if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.main()