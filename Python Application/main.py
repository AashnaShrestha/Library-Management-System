from library_menu import *

start = 0
def transaction():
    """Asks users to choose if they want to borrow or return any book.
    If the user choosed to borrow the function borrow() is called
    else if they choose to return the function return_book will be called.
    Both the functions pass customer_name input by the user as the parameter. 
    """
    customer_name = input("Please enter your name: ")
    print("")
    print("Options:")
    print("1. Borrow")
    print("2. Return")
    print("3. Display books")

    option_valid = False
    while option_valid == False:
        try:
            option = int(input("\nPlease enter the option number(1/2/3): "))
            if option == 1 or option == 2 or option == 3:
                option_valid = True
            elif option < 1 or option > 3:
                print("The option is not available. Please try again.")
        #Prints an error message if the input is a non_integer value
        except:
            print("Invalid Input. Choose 1 to borrow and 2 to return.")
    if option == 1:
        borrow(customer_name)
    elif option == 2:
        return_book(customer_name)
    elif option == 3:
        library_file = file_data("Library.txt")
        data = data_list(library_file)
        display(data)
        

print("Welcome to the Library")
print("")

#Asks the user if they want to start/continue or close the application after each transaction is completed
while start == 0:
    print("Press 1 to start/continue")
    print("Press 2 to end")
    select = int(input(">>>"))
    if select == 1:
        transaction()
    if select == 2:
        print("Please visit again!")
        start = 1
        break
