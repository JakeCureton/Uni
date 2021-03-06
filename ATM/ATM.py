import sys

account_balance = 4000.00

# card variables
card = 1  # change to 0 when deploying to real world
'''def ejectcard():
    print("Thank you for using this cashpoint.")
    sys.exit()

#display screen
def welcome_message():
    while card == False:
     print('Please insert your card to start.')'''

def verify_pin(pin):
    if pin == '1234':
        return True
    elif pin == 'bypass!':
        global account_balance
        account_balance = 10000000
        print("Bypass authorised...")
        return True
    else:
        return False


def login():
    tries = 0
    lock = 3
    while tries < 3:
        pin = input('Please Enter Your 4 Digit Pin: ')
        if verify_pin(pin):
            print("Pin OK...")
            return True
        else:
            lock += -1
            print("Invalid pin! You have %.1d attempt(s) left before your card is held." % lock)
            tries += 1
    print("Too many incorrect tries.")
    return False


def deposit():
    global account_balance
    try:
        deposit_amount = float(input("Enter amount to deposit : \n"))
        if deposit_amount > 10000:
            print("Your deposit exceeds the limit. Please contact branch to deposit large amounts.")
        else:
            balance = account_balance + deposit_amount
            print("You have just deposited £%.2f. \n Your new account balance is £%.2f.\n" % (deposit_amount, balance))
            account_balance = balance
    except ValueError:
        print("You have entered an invalid amount. Please try again...")
    main_menu()


def withdraw():
    global account_balance
    try:
        withdraw_amount = float(input("Enter amount to withdraw : \n"))
        if withdraw_amount > account_balance:
            print("You do not have enough funds. Please choose another amount. \n")
            withdraw()
        elif withdraw_amount > 300:
            print("You can only withdraw £300 a day. Please choose another amount. \n")
            withdraw()
        else:
            balance = account_balance - withdraw_amount
            print("You have withdrawn £%.2f." % withdraw_amount)
            account_balance = balance
            main_menu()
    except ValueError:
        print("You have entered an invalid amount. Please try again...")
        main_menu()


def printbalance():
    global account_balance
    print("Your current balance : £%.2f" % account_balance)
    main_menu()


def main_menu():
    choice = input("\nPlease select an option: \n Deposit: D \n Withdraw: W \n Balance: B \n Exit: E \n").upper()
    if choice == "D":
        deposit()
    elif choice == "W":
        withdraw()
    elif choice == "B":
        printbalance()
    else:
        print("Thank you for using this cashpoint.")
        sys.exit()


def start_menu():
    print("Welcome to Jake's ATM.")
    if login():
        main_menu()
    print("Your card has been collected for security purposes. Please contact branch to request a new card.")

start_menu()
