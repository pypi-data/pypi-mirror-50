def getweekday(day,month,year):
    import math


    month_final = ""

    if(month == "January" or month == 1):
        month_final = 0
    elif(month == "February" or month == 2):
        month_final = 3
    elif(month == "March" or month == 3):
        month_final = 3
    elif(month == "April" or month == 4):
        month_final = 6
    elif(month == "May" or month == 5):
        month_final = 1
    elif(month == "June" or month == 6):
        month_final = 4
    elif(month == "July" or month == 7):
        month_final = 6
    elif(month == "August" or month == 8):
        month_final = 2
    elif(month == "September" or month == 9):
        month_final = 5
    elif(month == "October" or month == 10):
        month_final = 0
    elif(month == "November" or month == 11):
        month_final = 3
    elif(month == "December" or month == 12):
        month_final = 5

    year_last2 = str(year)[-2:]
    year_last2_bet4 = math.trunc(int(year_last2)/4)
    year_last2_bet4_plus_year = year_last2_bet4 + int(year_last2)
    year_final = year_last2_bet4_plus_year % 7
    year_final = int(year_final)

    century_input = int(str(year)[:-2])

    if(century_input == 17):
        century_final = 4
    elif(century_input == 18):
        century_final = 2
    elif(century_input == 19):
        century_final = 0
    elif(century_input == 20):
        century_final = 6
    elif(century_input == 21):
        century_final = 4
    elif(century_input == 22):
        century_final = 2
    elif(century_input == 23):
        century_final = 0

    is_leap = False

    if(int(year) % 400 == 0):
        is_leap = True
    elif(int(year) % 4 == 0):
        is_leap = True
    else:
        is_leap = False

    final_number = day + month_final + year_final + century_final

    if(is_leap == True and month == "January" or month == "February"):
        final_number = final_number - 1


    if (final_number % 7 == 0):
        return("Sunday")
    elif (final_number % 7 == 1):
        return("Monday")
    elif (final_number % 7 == 2):
        return("Tuesday")
    elif (final_number % 7 == 3):
        return("Wednesday")
    elif (final_number % 7 == 4):
        return("Thursday")
    elif (final_number % 7 == 5):
        return("Friday")
    elif (final_number % 7 == 6):
        return("Saturday")

        return("Please, enter a valid date")
