import time

on_break = False

def serve():
    drink = input("What drink would you like?")
    if drink != "":
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Preparing your drink. Please wait...")
        time.sleep(2)
        print("Enjoy your", drink)
    else:
        print("Please enter a drink...")
        serve()

def verify_age():
    if not on_break:
        age = int(input("What is your age?"))
        if age >= 18:
            serve()
        else:
            print("Sorry, we cannot provide you with alcohol. You have to be 18 or over.")
    else:
        print("Sorry, there is no bartender to serve you. Please come back later.")

if __name__ == "__main__":
    verify_age()
