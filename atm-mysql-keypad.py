from datetime import datetime
import sys

import mysql.connector
from mysql.connector import errorcode

import RPi.GPIO as GPIO
import Keypad

import numpy as np

ROWS = 4
COLS = 4
keys =  [   '1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]

def pin_loop():
    global pin
    pin = []
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    
    keypad.setDebounceTime(50)      
    while(True):
        key = keypad.getKey()       
        if(key != keypad.NULL and not key == "#"):  
            pin.append(key)
            print("*")
        if(key == "*"):
            return("E")
        if(key == "A"):
            return("W")
        if(key == '#'):
            return(pin)
        
now = datetime.now()

time = now.strftime("%d/%m/%Y %H:%M:%S")

cnx = mysql.connector.connect(host = 'localhost',
                              user = 'atm',
                              password = 'cash_machine',
                              database = 'atm',
                              get_warnings = True
                              )
                              
try:
    
    customers = cnx.cursor()

    card_id = 4751280038571937 #simulate card in machine - must match card_id in db

    customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

    fetch = customers.fetchall()
    
    for row in fetch:
        global db_pin
        global account_balance
        global pin_add_comma
        name = row[0]
        db_pin = int(row[4])
        db_pin_check = []
        db_pin_check.append(db_pin)
        pin_add_comma = np.array(db_pin_check)
        account_balance = float(row[5])
        print ("Hi, ", name, ".")

    # card variables
    card = 1  # change to 0 when deploying to real world
    '''
    #display screen
    def welcome_message():
        while card == False:
         print('Please insert your card to start.')'''
    
    def change_pin():
        global card_id
        while True:
            try:
                pin1 = (input('Enter a new 4 digit pin: '))
                if len(pin1) != 4 and not pin1.isalpha():
                    raise ValueError
                pin2 = (input('Enter your new pin again:'))
                if len(pin2) != 4 or not pin1 == pin2:
                    print("Numbers do not match. Try again.")
                    change_pin()
                else:
                    customers = cnx.cursor()
                    customers.execute("""UPDATE customers SET card_pin=%s WHERE card_id=%s""", (pin1, card_id,))
                    cnx.commit()
                    print("Pin Changed.")
                    start_menu()
            except ValueError:
                print("Invalid pin. Please enter 4 numbers.")


    def verify_pin(pin):
        global db_pin_check
        pin_loop()
        if pin_add_comma == db_pin_check:
            return True
        else:
            return False


    def login():
        global db_pin
        customers = cnx.cursor()
        customers.execute("SELECT * FROM customers WHERE card_id=%s", (card_id,))

        fetch = customers.fetchall()
        lock = 3
        for row in fetch:
            pin = []
            tries = int(row[6])
        while tries < 3:
            print("Please Enter Your 4 Digit Pin: ")
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
        print ("\nPlease select an option: \n Deposit: D \n Withdraw: A \n Balance: B \n Pin Services: C \n Exit: E \n")
        keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    
        keypad.setDebounceTime(50)
        while(True):
            key = keypad.getKey()       
            if(key != keypad.NULL):  
                if(key == "#"):
                    print("Invalid selection")
                elif(key == "A"):
                    withdraw()
                elif(key == "B"):
                    print_balance()
                elif(key == "C"):
                    change_pin()
                elif(key == "D"):
                    deposit()
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
