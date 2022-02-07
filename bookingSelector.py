import mysql.connector
import sys
from termcolor import colored, cprint

# connects to the database and fetching the data from the table
def getDataFromDatabase():
    try:
        conn = mysql.connector.connect(
            user="airlineXreader",
            password="GB5zo5WzS0GTx&R4TY",
            host="wi-winf.htwsaar.de",
            port=13307,
            database="airlineX"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    conn.autocommit = True
    cur.execute("SELECT * FROM flightbookings ORDER BY price DESC")

    # convert the result to a list of tuples
    rows = list(cur)

    # generate an empty list
    resultList = []
    for row in rows:
        resultList.append(list(row))

    #close the db connection
    cur.close()
    conn.close()

    return resultList

# Read the data from the central location:
bookingList = getDataFromDatabase()


#Function to create new lists for each category
def new_List(bookingList, category):
    newList=[]
    for i in range(0,len(bookingList)):
        if bookingList[i][5] == category:
            newList.append(bookingList[i])
    return newList

#Calling the new_list function to create separate lists for each booking class.
FirstClassBookings = new_List(bookingList,'F')
BusinessClassBookings = new_List(bookingList,'B')
EconomyClassBookings = new_List(bookingList,'Y')

# sorting each new list according to price desc and year asc
FirstClassBookings = sorted(FirstClassBookings, key = lambda x: (-x[6],x[4]))
BusinessClassBookings = sorted(BusinessClassBookings, key = lambda x: (-x[6],x[4]))
EconomyClassBookings = sorted(EconomyClassBookings, key = lambda x: (-x[6],x[4]))

#Start interaction with user and provide welcome screen
print(colored("\nWelcome! I am here to help you with your bookings!".title(), 'yellow'))
print(colored("""
\ `/ |
 \__`!
 / ,' `-.____________________________
'-'\_____ SAP Phython Flight School   `-.
   <____()-=O=O=O=O=O=[]==O==O==O===O==--)
     `.___ ,-----,__________________...-'
          /    .'
         /   .'
        /  .'         
        `-'""",'yellow'))

#Create a function that can be called to collect and validate the user input
#Check are performed to ensure a number is provided - no alpha allowed
#Null entry will not be accepted but zero seats are accepted.
def userInput():
    while True:
        N_FirstClass = input('\n Please, let me know how many people should sit in First Class: ')
        try:
            N_FirstClass = int(N_FirstClass)
            if N_FirstClass < 0:
                print('Please, try again with positive number of seats for First Class.')
                continue
            else:
                break
        except ValueError:
            print('Please, try again with the valid number of seats for First Class.')
            continue
    while True:
        N_BusinessClass = input('\n Thank you, now let me know the number of seats in Business Class: ')
        try:
            N_BusinessClass = int(N_BusinessClass)
            if N_BusinessClass < 0:
                print('Please, try again with positive number of seats for Business Class.')
                continue
            else:
                break
        except ValueError:
            print('Please, try again with the valid number of seats for Business Class.')
            continue
    while True:
        N_EconomyClass = input('\n Thank you, now let me know the number of tiny seats in Economy Class: ')
        try:
            N_EconomyClass = int(N_EconomyClass)
            if N_EconomyClass < 0:
                print('Please, try again with positive number of seats for Economy Class.')
                continue
            else:
                break
        except ValueError:
            print('Please, try again with the valid number of seats for Economy Class.')
            continue
    #return the output for the function
    return N_FirstClass, N_BusinessClass, N_EconomyClass


#Call the function to read the user input for the seats available in all three the classes
N_FirstClass, N_BusinessClass, N_EconomyClass = userInput()

# Validation for total nr of seats - check against length of list - not relevant for now
'''
if N_FirstClass + N_BusinessClass + N_EconomyClass > len(bookingList):
    check = False
if N_FirstClass + N_BusinessClass + N_EconomyClass <= len(bookingList):
    check = True
while check == False:
    print("\nThere are only limited available bookings, please make sure your input is less than", len(bookingList))
    N_FirstClass, N_BusinessClass, N_EconomyClass = userInput()
    if N_FirstClass + N_BusinessClass + N_EconomyClass > len(bookingList):
        check = False
    if N_FirstClass + N_BusinessClass + N_EconomyClass <= len(bookingList):
        check = True
        print("\nThank you!")
'''

#Counting average price according to a booking we will need this as selection criteria
def average_price(bookingList, category):
    sum = 0
    n = 0
    for i in range(0,len(bookingList)):
        if bookingList[i][5] == category:
            sum = bookingList[i][6] + sum
            n += 1
    average= sum/n
    return average

#Counting Min price according to a booking category, this was neccessery to check if our selection criteria will work for other categories.
# example: average price of first class > min price of business class, etc. NOT RELEVANT FOR NOW
'''
def min_price(bookingList, category):
    min = bookingList[0][6]
    for i in range(0,len(bookingList)):
       if bookingList[i][5] == category:
            if bookingList[i][6] < min:
                min = bookingList[i][6]
    return min

#Counting Max price according to a booking category
def max_price(bookingList, category):
    max = 0
    for i in range(0,len(bookingList)):
       if bookingList[i][5] == category:
            if bookingList[i][6] > max:
                max = bookingList[i][6]
    return max
'''

#Filter for First class
#  F1 criteria 1)price above average, Senator status and oldest passengers
#  F2 criteria 1)price above average and Senator status (any age)
#  F3 criteria 1)price above average
#  F4 Anyone available
# Due to the unknown number of seats on the plane each check must be completed for the full list before the next can start
def filterFirstClass(FirstClassBookings):
    cprint("\nThe data for first class is being processed: ",'blue')
    global N_FirstClass, total_price
    EAvPrice = 0
    n=0
    if N_FirstClass == 0:
        cprint("So sorry, due to COVID19 pandemic, there are no First Class seats on this plane.",'blue')
    else:
        for booking in FirstClassBookings:
            if N_FirstClass ==0:
                break
            if booking[9] == '': #selection critera one checking for people who arent seated
                if booking[6] >= average_price(bookingList,'F') and booking[8] == 1 and booking[4]<= 1970: #old people with senator status
                    booking[9] = "Booked F1"
                    cprint(f'\t\t\t{booking[9]}', 'blue', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'blue', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'blue', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'blue', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'blue', end='')
                    cprint(f'\t\tSenator', 'blue')
                    N_FirstClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in FirstClassBookings:
            if N_FirstClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList,'F') and booking[8] == 1: # any age with senator status
                    booking[9] = "Booked F2"
                    cprint(f'\t\t\t{booking[9]}', 'blue', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'blue', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'blue', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'blue', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'blue', end='')
                    cprint(f'\t\tSenator', 'blue')
                    N_FirstClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in FirstClassBookings:
            if N_FirstClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList,'F') and booking[8] == 0: #people without senator status but high price
                    booking[9] = "Booked F3"
                    cprint(f'\t\t\t{booking[9]}', 'blue', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'blue', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'blue', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'blue', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'blue')
                    N_FirstClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in FirstClassBookings:
            if N_FirstClass == 0:
                break
            if booking[9] == '':
               # if booking[6] < average_price(bookingList,'F'): #anyone
                  booking[9] = "Booked F4"
                  cprint(f'\t\t\t{booking[9]}', 'blue', end='')
                  cprint(f'\t\t{booking[1]:<15} ', 'blue', end='')
                  cprint(f'\t\t{booking[2]:<15}', 'blue', end='')
                  cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'blue', end='')
                  cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'blue')
                  N_FirstClass -= 1
                  EAvPrice += booking[6]
                  n += 1
    if n != 0:
        cprint("\nFirst Class is now fully booked! ",'blue')
    total_price = EAvPrice
    if n > 0:
        EAvPrice = int(EAvPrice/n)
    else:
        EAvPrice = 0
    cprint(f'\nAverage price for {n} seats in First Class category is {EAvPrice}', 'blue')

#Filter for Business class
#  B1 criteria 1)price above average, Senator status and oldest passengers
#  B2 criteria 1)price above average and Senator status (any age)
#  B3 criteria 1)price above average
#  B4 Anyone available
def filterBusinessClass(BusinessClassBookings):
    cprint(f"\nWe are ready to start with Business Class: Please enter to proceed: ",'magenta', end='')
    proceed = input()
    global N_BusinessClass, total_price
    EAvPrice = 0
    n = 0
    if N_BusinessClass == 0:
        cprint("Sorry for this, but there are no Business Class seats on this plane",'magenta')
    else:
        for booking in BusinessClassBookings:
            if N_BusinessClass == 0:
                break
            if booking[9] == '':  # selection criteria one checking for people who arent seated
                if booking[6] >= average_price(bookingList, 'B') and booking[8] == 1 and booking[4] <= 1976:  # old people with senator status
                    booking[9] = "Booked B1"
                    cprint(f'\t\t\t{booking[9]}', 'magenta', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'magenta', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'magenta', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'magenta', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'magenta',end='')
                    cprint(f'\t\tSenator', 'magenta')
                    N_BusinessClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in BusinessClassBookings:
            if N_BusinessClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList, 'B') and booking[8] == 1:  # any age with senator status
                    booking[9] = "Booked B2"
                    cprint(f'\t\t\t{booking[9]}', 'magenta', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'magenta', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'magenta', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'magenta', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'magenta',end='')
                    cprint(f'\t\tSenator', 'magenta')
                    N_BusinessClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in BusinessClassBookings:
            if N_BusinessClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList, 'B') and booking[8] == 0:  # people without senator status but high price
                   booking[9] = "Booked B3"
                   cprint(f'\t\t\t{booking[9]}', 'magenta', end='')
                   cprint(f'\t\t{booking[1]:<15} ', 'magenta', end='')
                   cprint(f'\t\t{booking[2]:<15}', 'magenta', end='')
                   cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'magenta', end='')
                   cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'magenta')
                   N_BusinessClass -= 1
                   EAvPrice += booking[6]
                   n += 1
        for booking in BusinessClassBookings:
            if N_BusinessClass == 0:
                break
            if booking[9] == '':
                if booking[6] < average_price(bookingList, 'B'):  # anyone
                    booking[9] = "Booked B4"
                    cprint(f'\t\t\t{booking[9]}', 'magenta', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'magenta', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'magenta', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'magenta', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'magenta')
                    N_BusinessClass -= 1
                    EAvPrice += booking[6]
                    n += 1
    total_price += EAvPrice
    if n != 0:
        cprint("\nBusiness Class is now fully booked! ", 'magenta')
    if n > 0:
        EAvPrice = int(EAvPrice / n)
    else:
        EAvPrice = 0
    cprint(f'\nAverage price for {n} seats in Business Class category is {EAvPrice}', 'magenta')

#Filter for Economy class
#  E1 criteria 1)price above average, Senator status and oldest passengers
#  E2 criteria 1)price above average and Senator status (any age)
#  E3 criteria 1)price above average
#  E4 Anyone available
def filterEconomyClass(EconomyClassBookings):
    cprint(f"\nWe are ready to start with Economy Class: Please enter to proceed: ",'green', end='')
    proceed = input()
    global N_EconomyClass, total_price
    EAvPrice = 0
    n=0
    if N_EconomyClass == 0:
        cprint('Must be flying lots of cargo today, there are no Economy Class seats on this plane.','green')
    else:
        for booking in EconomyClassBookings:
            if N_EconomyClass ==0:
                break
            if booking[9] == '': #selection critera one checking for people who arent sitting
                if booking[6] >= average_price(bookingList,'Y') and booking[8] == 1 and booking[4]<= 1970: #old people with senator status
                    booking[9] = "Booked E1"
                    cprint(f'\t\t\t{booking[9]}', 'green', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'green', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'green', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'green', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'green',end='')
                    cprint(f'\t\tSenator', 'green')
                    N_EconomyClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in EconomyClassBookings:
            if N_EconomyClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList,'Y') and booking[8] == 1: # any age with senator status
                    booking[9] = "Booked E2"
                    cprint(f'\t\t\t{booking[9]}', 'green', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'green', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'green', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'green', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'green',end='')
                    cprint(f'\t\tSenator', 'green')
                    N_EconomyClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in EconomyClassBookings:
            if N_EconomyClass == 0:
                break
            if booking[9] == '':
                if booking[6] >= average_price(bookingList,'Y') and booking[8] == 0: #people without senator status but high price
                    booking[9] = "Booked E3"
                    cprint(f'\t\t\t{booking[9]}', 'green', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'green', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'green', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'green', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'green')
                    N_EconomyClass -= 1
                    EAvPrice += booking[6]
                    n += 1
        for booking in EconomyClassBookings:
            if N_EconomyClass == 0:
                break
            if booking[9] == '':
                if booking[6] < average_price(bookingList,'Y'): #anyone
                    booking[9] = "Booked E4"
                    cprint(f'\t\t\t{booking[9]}', 'green', end='')
                    cprint(f'\t\t{booking[1]:<15} ', 'green', end='')
                    cprint(f'\t\t{booking[2]:<15}', 'green', end='')
                    cprint(f'\t\tPrice in Euro = {booking[6]:<4}', 'green', end='')
                    cprint(f'\t\t Aged {2021 - booking[4]:<2}', 'green')
                    N_EconomyClass -= 1
                    EAvPrice += booking[6]
                    n += 1
    total_price += EAvPrice
    if n != 0:
        cprint("\nEconomy Class is now jam packed! ", 'green')
    if n > 0:
        EAvPrice = int(EAvPrice / n)
    else:
        EAvPrice = 0
    cprint(f'\nAverage price for {n} seats in Economy category is {EAvPrice}','green')

#Check for minors in the bookinglist.
#Due to missing guardianship indicators in the source data the children might get separated from their parents/caretakers
#The only possibility is to list possible matching Surnames but this is not garuanteed to find find the parents
#It is more likely that this link will be maintained in a separate indicator ie ID-number references that are not available.
#As a workaround we try to raise a flag for the booking crew to match minors manually with parents before the booking is confirmed.
#bookingList = sorted(bookingList, key = lambda x: (x[1],x[4]))
minorList = filter(lambda x: [row for row in bookingList if x[4] > 2008], bookingList)
cprint('\n\nPlease, note that the following minors need to be placed with their guardians!')
cprint('Please, ensure that they are correctly seated before the final bookings are released:')
for entry in minorList:
    cprint(f'\t\t\t{entry[9]}', 'red', end='')
    cprint(f'\t\t{entry[1]:<15} ', 'red', end='')
    cprint(f'\t\t{entry[2]:<15}', 'red', end='')
    cprint(f'\t\t Booking Class: {entry[5]:<15}', 'red', end='')
    cprint(f'\t\t Aged {2021 - entry[4]:<2}', 'red')
cprint('\n\nPlease, acknowledge the above warning and press enter to proceed:',end='')
proceed = input()


#Call the function to run the filter for First Class and produce output at same time
filterFirstClass(FirstClassBookings)
#Call the function the run the filter for Business Class
filterBusinessClass(BusinessClassBookings)
#Call the function to run the filter for Economy Class
filterEconomyClass(EconomyClassBookings)

cprint('All system bookings are completed - please press enter to proceed:',end='')
proceed = input()

cprint(f"\nThe total price for all bookings on this plane is: {total_price}",'yellow')

cprint(f"\n\t\t**Your flight is ready for departure. Bon Voyage**",'yellow')
cprint(f"""
                            |
                           -'-
                          '   '
                     ----'  o  '----
          ---------------'     '---------------
                (   )      ' '      (   )
                 '.'                 '.'

""",'yellow')
