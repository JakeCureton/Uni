def main():
    ph = float(input("Please enter your pH value."))
    if ph >= 8:
        print("Your substance pH is an alkaline.")
    elif ph == 7:
        print("Your subtance pH is neutral.")
    elif ph <= 6:
        print("Your substance pH is an acid.")
    elif ph > 14:
        print("Please enter a value equal to or less than 14.")
        main()
    elif ph < 0:
        print("Please enter a value equal to or more than 0.")
        main()

if __name__ == "__main__":
    main()
