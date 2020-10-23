from datetime import datetime
import sys

import mysql.connector
from mysql.connector import errorcode

now = datetime.now()

time = now.strftime("%d/%m/%Y %H:%M:%S")

cnx = mysql.connector.connect(host = 'localhost',
                              user = 'cash_machine',
                              password = 'test',
                              database = 'atm',
                              get_warnings = True
                              )
                              
try:

    customers = cnx.cursor()

    card_id = 4751280038571937 #simulate card in machine - must match card_id in db

    customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

    fetch = customers.fetchall()
    # need to add successful login attempts since last correct login to db (3 max)
    for row in fetch:
        global db_pin
        global account_balance
        name = row[0]
        db_pin = int(row[4])
        account_balance = float(row[5])
        print ("Hi, ", name, ".")

    # card variables
    card = 1  # change to 0 when deploying to real world
    '''
    #display screen
    def welcome_message():
        while card == False:
         print('Please insert your card to start.')'''


    def verify_pin(pin):
        global db_pin
        if pin == db_pin:
            return True
        else:
            return False


        def login():
        customers = cnx.cursor()
        customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

        fetch = customers.fetchall()
        lock = 3
        for row in fetch:
            tries = int(row[6])
        while tries < 3:
            global db_pin
            pin = int(input('Please Enter Your 4 Digit Pin: '))
            if verify_pin(pin):
                customers = cnx.cursor()
                customers.execute("""UPDATE customers SET pin_tries="0" WHERE card_id=%s""", (card_id,))
                cnx.commit()
                print("Pin OK...")
                return True
            elif tries == 3:
                return False
                print("Thank you for using this cashpoint.")
                sys.exit()
            else:
                tries = tries - -1
                lock = lock + - 1
                customers = cnx.cursor()
                customers.execute("""UPDATE customers SET pin_tries=%s WHERE card_id=%s""", (tries, card_id,))
                cnx.commit()
                print("Invalid pin! You have %.1d attempt(s) left before your card is held." % lock)
        print("Too many incorrect tries.")
        return False


    def deposit():
        global account_balance
        global card_id
        try:
            deposit_amount = float(input("Enter amount to deposit : \n"))
            if deposit_amount > 10000:
                print("Your deposit exceeds the limit. \nPlease see desk at branch to deposit large amounts.")
            else:
                balance = account_balance + deposit_amount
                print("You have just deposited £%.2f. \nYour new account balance is £%.2f.\n" % (deposit_amount, balance))
                customers = cnx.cursor()
                customers.execute("""UPDATE customers SET balance=%s WHERE card_id=%s""", (balance, card_id,))
                cnx.commit()
                account_balance = float(row[5])
        except ValueError:
            print("You have entered an invalid amount. Please try again...")
        main_menu()


    def withdraw():
        global account_balance
        global card_id
        try:
            withdraw_amount = float(input("Enter amount to withdraw : \n"))
            customers = cnx.cursor()
            customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

            fetch = customers.fetchall()

            for row in fetch:
                global withdraw_limit
                withdraw_limit = int(row[3])
                last_withdraw = withdraw_limit + withdraw_amount
            if withdraw_amount > account_balance:
                print("You do not have enough funds. Please choose another amount. \n")
                withdraw()
            elif last_withdraw > 300:
                print("You can only withdraw £300 a day. Please choose another amount. \n")
                start_menu()
            else:
                balance = account_balance - withdraw_amount
                print("You have withdrawn £%.2f." % withdraw_amount)
                customers = cnx.cursor()
                customers.execute("""UPDATE customers SET last_withdraw=%s, balance=%s WHERE card_id=%s""", (last_withdraw, balance, card_id,))
                cnx.commit()
                account_balance = float(row[5])
                main_menu()
        except ValueError:
            print("You have entered an invalid amount. Please try again...")
            main_menu()


    def print_balance():
        customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

        fetch = customers.fetchall()

        for row in fetch:
            global account_balance
            account_balance = float(row[5])
            print("Your current balance : £%.2f" % account_balance)
            main_menu()


    def main_menu():
        choice = input("\nPlease select an option: \n Deposit: D \n Withdraw: W \n Balance: B \n Exit: E \n").upper()
        if choice == "D":
            deposit()
        elif choice == "W":
            withdraw()
        elif choice == "B":
            print_balance()
        else:
            print("Thank you for using this cashpoint.")
            sys.exit()


    def start_menu():
        print("Welcome to Jake's ATM.")
        if login():
            main_menu()
        print("Your card has been collected for security purposes. Please contact branch to request a new card.")

    start_menu()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
