import streamlit as st
import uuid
import datetime

class BankAccount:
    def __init__(self, account_holder_name, initial_balance=0.0, account_type="Savings"):
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_number = str(uuid.uuid4())
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.creation_date = datetime.date.today()

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balance += amount
        self._add_transaction("Deposit", amount)
        return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
        return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    def get_balance(self):
        return self.balance

    def get_account_details(self):
        details = f"Account Number: {self.account_number}\n"
        details += f"Account Holder: {self.account_holder_name}\n"
        details += f"Account Type: {self.account_type}\n"
        details += f"Balance: ${self.balance:.2f}\n"
        details += f"Creation Date: {self.creation_date}\n"
        return details

    def _add_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        self.transactions.append(
            {"timestamp": timestamp, "type": transaction_type, "amount": amount}
        )

    def get_transaction_history(self):
        return self.transactions

    def format_transaction_history(self):
        if not self.transactions:
            return "No transactions yet."

        history_text = "-" * 30 + "\nTransaction History:\n" + "-" * 30 + "\n"
        for transaction in self.transactions:
            history_text += (
                f"{transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{transaction['type']:<10}: ${transaction['amount']:>8.2f}\n"
            )
        history_text += "-" * 30
        return history_text


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_holder_name, initial_balance=0.0, account_type="Savings"):
        try:
            account = BankAccount(account_holder_name, initial_balance, account_type)
            self.accounts[account.account_number] = account
            return f"Account created successfully. Account number: {account.account_number}"
        except (TypeError, ValueError) as e:
            return f"Account creation failed: {e}"

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted successfully."
        else:
            return f"Account {account_number} not found."

    def list_all_accounts(self):
        if not self.accounts:
            return "No accounts in the system."

        accounts_text = "-" * 30 + "\nList of All Accounts:\n" + "-" * 30 + "\n"
        for account_number, account in self.accounts.items():
            accounts_text += account.get_account_details() + "-" * 30 + "\n"
        return accounts_text


banking_system = BankingSystem()

st.title("Banking System")

menu = ["Create Account", "Deposit", "Withdraw", "Check Balance", "Account Details", "Transaction History", "List All Accounts", "Delete Account"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Create Account":
    st.subheader("Create Account")
    account_holder_name = st.text_input("Account Holder Name")
    initial_balance = st.number_input("Initial Balance", min_value=0.0, value=0.0)
    account_type = st.selectbox("Account Type", ["Savings", "Checking"])
    if st.button("Create"):
        message = banking_system.create_account(account_holder_name, initial_balance, account_type)
        st.success(message)

elif choice == "Deposit":
    st.subheader("Deposit")
    account_number = st.text_input("Account Number")
    amount = st.number_input("Amount", min_value=0.0, value=0.0)
    if st.button("Deposit"):
        account = banking_system.get_account(account_number)
        if account:
            message = account.deposit(amount)
            st.success(message)
        else:
            st.warning("Account not found.")

elif choice == "Withdraw":
    st.subheader("Withdraw")
    account_number = st.text_input("Account Number")
    amount = st.number_input("Amount", min_value=0.0, value=0.0)
    if st.button("Withdraw"):
        account = banking_system.get_account(account_number)
        if account:
            message = account.withdraw(amount)
            st.success(message)
        else:
            st.warning("Account not found.")

elif choice == "Check Balance":
    st.subheader("Check Balance")
    account_number = st.text_input("Account Number")
    if st.button("Check Balance"):
        account = banking_system.get_account(account_number)
        if account:
            balance = account.get_balance()
            st.success(f"Current balance: ${balance:.2f}")
        else:
            st.warning("Account not found.")

elif choice == "Account Details":
    st.subheader("Account Details")
    account_number = st.text_input("Account Number")
    if st.button("Get Details"):
        account = banking_system.get_account(account_number)
        if account:
            details = account.get_account_details()
            st.text(details)
        else:
            st.warning("Account not found.")

elif choice == "Transaction History":
    st.subheader("Transaction History")
    account_number = st.text_input("Account Number")
    if st.button("Get History"):
        account = banking_system.get_account(account_number)
        if account:
            history_text = account.format_transaction_history()
            st.text(history_text)
        else:
            st.warning("Account not found.")

elif choice == "List All Accounts":
    st.subheader("List All Accounts")
    if st.button("List Accounts"):
        accounts_text = banking_system.list_all_accounts()
        st.text(accounts_text)

elif choice == "Delete Account":
    st.subheader("Delete Account")
    account_number = st.text_input("Account Number")
    if st.button("Delete"):
        message = banking_system.delete_account(account_number)
        st.success(message)
