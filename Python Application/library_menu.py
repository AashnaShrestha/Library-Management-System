from read_data import *
def display(data):
    for i in range(len(data)):
        print(data[i][0])
    
def borrow(customer_name):
    """Actions to be performed when a book is to be borrowed
    The function takes the parameter customer_name.
    Takes input from user for the book to be borrowed.
    Generates a txt file with transaction details.
    Updates the stock of the books once they are borrowed.
    """

    #Calling the function file_data() and data_list() from read_data.py
    fileData = file_data("Library.txt")
    data = data_list(fileData)
    
    for i in range(len(data)):
        for j in range(2, 4):
            data[i][j] = int(data[i][j])
            
    print("Book List: ")
    print("")
    print("[Book's Name, Author, Quantity, Price in Rs.]")
    for row in data:
        print(row)     #Printing the booklist
    print("") 

    transaction = {}   #Dictionary to store transaction details

    #Import date and time
    from datetime import date, timedelta
    borrow_date = date.today()
    return_date = borrow_date + timedelta(days=10)

    #Data for dictionary
    transaction["Name"] = customer_name
    transaction["Borrow Date"] = borrow_date
    transaction["Return Date"] = return_date

    #Getting the number of books to be borrowed input by the user
    count = 0
    while count == 0:
        try:
            num_of_books = int(input("Number of books to be borrowed: "))
            if num_of_books > 0:
                count = 1
            elif num_of_books <= 0:
                print("Negative numbers are not valid. Please try again.")
        except:
            print("Invalid Input. Please enter a valid number.")
    print("")
    
    book_available = False
    total_amount = 0
    books = 0
    while books < num_of_books:
        book_name = input("Name of the book: ")
        books+=1
        for i in range(len(data)):
            for j in range(1):
                '''Checks if the book is available.
                Calculates the total amount and updates the stock.
                '''
                if book_name == data[i][j] and data[i][2] > 0:
                    price = data[i][3]
                    transaction[data[i][0]] = price
                    total_amount += price
                    stock = data[i][2] - 1
                    data[i][2] = stock
                    book_available = True
            
        
    transaction["Total Amount"] = total_amount

    '''Checks if the file with the transaction id exists.
    Increments the transaction id if the id exists already.
    '''
    import os
    transaction_id = 1
    while os.path.exists(f"Transaction_{transaction_id}.txt"):
        transaction_id += 1
    transaction["Transaction ID"] = transaction_id
        
    
    if book_available == True:
        '''Opens a txt file with the name as Transaction_transaction_id in write mode.
            Writes the details of the transaction in the file.'''
        file = open(f"Transaction_{transaction_id}.txt", "w")  
        file.write("Borrow Transaction: \n")
        print("\nBook Details:")
        for key, value in transaction.items():
            transaction_details = key+" : "+str(value)
            file.write(transaction_details)
            file.write("\n")
            print(transaction_details)
        file.close()

        for i in range(len(data)):
            for j in range(2, 4):
                data[i][j] = str(data[i][j]) 

        #Updates the data with new stock in the file "Library.txt"
        main_file = open("Library.txt", "w")
        for items in data:
            data_update = ",".join(items)
            main_file.write(data_update+"\n")
        main_file.close()

        print("\nThank you for borrowing")
    elif book_available == False:
        print(book_name, "is not available")  #Error message in case the book entered by the user is not available.


def return_book(customer_name):
    """Actions to be performed when a book is to be returned.
    The function takes the parameter customer_name.
    Takes input from user for the book to be returned.
    Finds the txt file with the details when the book was borrowed and writes the details of return in it
    Updates the stock of the books once they are returned.
    """

    #Calling the function file_data() and data_list() from read_data.py
    library_file = file_data("Library.txt")
    library_data = data_list(library_file)

    #Converts the price and range into integer 
    for i in range(len(library_data)):
        for j in range(2, 4):
            library_data[i][j] = int(library_data[i][j])

    #Getting the number of books to be returned input by the user        
    count = 0
    while count == 0:
        try:
            num_of_books = int(input("Number of books to be returned: "))
            if num_of_books > 0:
                count = 1
            elif num_of_books <= 0:
                print("Please enter a valid number")
        except:
            print("Please enter a valid number")
            
    total_amount = 0
    fine = 0
    transaction = {}
    transaction["Customer's Name"] = customer_name
    books = 0
    
    while books < num_of_books:
        transaction_found = False
        books +=1
        while transaction_found == False:
            '''Print the details of the transaction with the id input by the user.
            Display and error message if the file is not available.
            '''
            try:
                transaction_id = input("Enter Transaction ID: ")
                transaction_file = file_data(f"Transaction_{transaction_id}.txt")
                transaction_data = data_list(transaction_file)
                display(transaction_data)
                transaction_found = True
            except:
                print("Transaction ID not found")
    

        book_name = input("Name of the book: ")
        book_found = False
        book_returned = False
        
        for i in range(len(library_data)):
            for j in range(1):
                if book_name == library_data[i][j]:
                    transaction["Book"] = library_data[i][0]
                    price = library_data[i][3]   #Getting the price of the book entered by the user

                    book_status = book_name + " : Returned"
                    for x in range(len(transaction_data) - 1):
                        #Prints an error message if the book entered by the user has been returned already
                        if transaction_data[x][0] == book_status:
                            print("The book has been returned already")
                            book_returned = True

                        else:
                            book_detail = book_name + " : " + str(price)
                            if transaction_data[x][0] == book_detail:
                                book_found = True
                                
                                return_date = transaction_data[3][0]
                                return_date_string = return_date[14:24]
                                
                                from datetime import datetime, date, timedelta
                                #Converts return_date_string to yyyy/mm/dd format
                                return_date_object = datetime.strptime(return_date_string, '%Y-%m-%d').date()

                                current_date = date.today()  #Getting the current date

                                '''Checks if the date to return the book has passed.
                                Adds a fine to the total amount if the date has passed.
                                '''
                                if current_date <= return_date_object:
                                    amount = price
                                elif current_date > return_date_object:
                                    date_passed = (current_date - return_date_object).days
                                    fine = 50 * date_passed
                                    amount = price + fine

                                stock = library_data[i][2] + 1
                                library_data[i][2] = stock

                                total_amount += amount

                                #Data for dictionary
                                transaction["Return Date"] = current_date                
                                transaction["Fine"] = fine
                                transaction["Total Amount"] = total_amount
                                transaction[book_name] = "Returned"
            
        if book_found == True and book_returned == False:
            '''Opens a txt file with the name as Transaction_transaction_id in append mode.
            Updates the return details of the transaction in the file.
            '''
            print("\nBook Details:")
            file = open(f"Transaction_{transaction_id}.txt", "a")
            file.write("\nReturn Transaction: \n")
            for key, value in transaction.items():
                transaction_details = key+" : "+str(value)
                file.write(transaction_details)
                file.write("\n")
                print(transaction_details)
            file.write("\n")
            file.close()

            #Updates the data with new stock in the file "Library.txt"
            for i in range(len(library_data)):
                for j in range(2, 4):
                    library_data[i][j] = str(library_data[i][j]) 
            main_file = open("Library.txt", "w")
            for items in library_data:
                data_update = ",".join(items)
                main_file.write(data_update+"\n")
            main_file.close()
            print("\nBook Returned")

        elif book_found == False:
                #Error message to be displayed if the book's name entered by the user is not found in the file
                print("The transaction list does not match. \n Please check the book's name and the Transaction ID")


        
            
