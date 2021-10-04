"""
This program incorporates a cleansing process of analysing each record of a
CSV file, and comparing it to defined paramentres for each coloumn, if the
reocrd is deemed as incorrect the row will be considered as corrupted, and a
corrupt will be written to the added coloumn of the CSV file. 
"""

#describes inside lines of code

__author__ = "Nikhil Naik "


from assign1_utilities import get_column, replace_column, truncate_string
 
    
def check_first_name(row,corrupted):
    """Checks that the first name has the correct parametres, that also
    includes a list of exceptions of special characters and
    and that the name is less than 31 characters and
    rectifies it if needed, and passes a value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated first name at indicated coloumn for each row
    Preconditions:
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        firstname is a none, "", string

    """
    list_of_exceptions = ["-","'", " "]
    newstring = get_column(row, 1)
    first_name_length = len(newstring)
    i = 0
    part_of_doc = False
    while i < first_name_length and corrupted == False:
        if newstring[i] in list_of_exceptions:
            part_of_doc = True
        else:
            pass
        i = i + 1
            
    if part_of_doc == False:        #only enters if not containg special chars
        if newstring == None or newstring == "":
            newstring = newstring
            corrupted = True
        elif first_name_length > 31:
            newstring = truncate_string(newstring, 30)
        elif newstring.isalpha() == False:
            newstring = newstring
            corrupted = True
   

    return replace_column(row, newstring, 1), corrupted
       
def check_place(row,corruptplace):
    """Checks that the place has the correct parametres and passes a value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated placing at indicated coloumn for each row
    Preconditions:
        row <> Nothing or empty
        place is a none, "", string
        place length name is >0

    """
    corruptplace = False
    place_string = get_column(row, 4)
    place_length = len(place_string)
    correct_place = False
    if place_string == None or place_string == "":
        place_string = place_string
    elif place_string.isdigit() == True and place_length >3:
        place_string = place_string
        corruptplace = True
    elif place_string.isalpha() == True and place_length < 3:
        corruptplace = True
    elif place_string == "DNF" or place_string == "DNS" or place_string == "PEN":
        corruptplace = False

    return replace_column(row, place_string,4),corruptplace
        
    




    
def check_event_name(row,corruptevent):
    """Checks that the event name has the correct parametres  changes
    it if needed to a reduced 30 character length and passes a value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated event name at indicated coloumn for each row
    Preconditions:
        row <> Nothing or empty
        coloumn_number is >= 0  or <= last coloumn
        event name is a none or  "" or a string
        eventlength is > 0

    """
    list_of_incorrect_char = ["$", "#", "@", "&", "*", "!"]
    part_of_list = False
    i = 0
    corruptevent = False
    newevent = get_column(row, 0)
    event_length = len(newevent)
    while i < event_length and part_of_list == False:
        if newevent[i] in list_of_incorrect_char:
            part_of_list = True
        i = i + 1
    
    if newevent == None or newevent == "":
        newevent = newevent
        corruptevent = True
    elif event_length > 31 and part_of_list == False:
        newevent = truncate_string(newevent, 30)
    elif part_of_list == True: 
        corruptevent = True
                              
  
        
        

    return replace_column(row, newevent, 0),corruptevent
       
def check_medal(row,corruptmedel):
    """Checks that the medel has the correct parametres  and
    and that the  medel is existant  is first captilized and
    than lowercase characters 
    rectifies it if needed, and passes a value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated medel string at indicated coloumn for each row
    Preconditions:
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        medel length is >0
        medel is a none, "", string

    """
    corruptmedel = False
    placing_string = get_column(row, 4)
    medel = get_column(row, 7)
    if medel == None or medel == "" and placing_string != "3" and placing_string !="1" and placing_string!="2" :
        medel = ""
    elif placing_string == "3" and medel == None:
        corruptmedel = True
    elif placing_string == "2" and medel == None:
        corruptmedel = True
    elif placing_string == "1" and medel == None:
        corruptmedel = True
    elif medel.upper() == "GOLD" and placing_string =="1" :
        medel = "Gold"
    elif medel.upper() == "SILVER" and placing_string == "2":
        medel = "Silver"
    elif medel.upper() == "BRONZE" and placing_string == "3":
        medel = "Bronze"
    else:
        corruptmedel = True

    return replace_column(row, medel, 7),corruptmedel
    
def check_coloumn_eleven_and_ten(row, corrupted_ten_eleven):
    """Checks that the rows eleven and ten correspond, if the row
    11 contains data, than row 10 must have the same data, else the row
    is deemed as corrupted, hence passsing a corrupt parametre.
     
    Parametres :
        row(str): String of data in a CSV format
        corrupted_ten_eleven(BOOL):a true or false boolean of the validity of
        the check

    Return:
        str: Updated the row, as well as the validity of the row
    Preconditions:
        row is >= 0
        coloumn_number is an 8 or 9
        row <> Nothing or empty
        coloumn 11 or 10 is nothing, float, digit, string, ""

    """
    corrupted_ten_eleven = False
    string_ten = get_column(row, 8)
    string_eleven = get_column(row, 9)
    if string_eleven == string_ten:
        corrupted_ten_eleven = False
    elif string_eleven == None or string_eleven == "":
        corrupted_ten_eleven = False
    else:
        corrupted_ten_eleven = True
                
    return row, corrupted_ten_eleven 
    
def check_lastname(row,corrupt_last_name):
    """Checks that the Last name has the correct parametres  and
    and that the  last name is less than 31 characters and
    rectifies it if needed, and passes a value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated last name at indicated coloumn for each row
    Preconditions:
        namelength is > 0
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        lastname is a none, "", string

    """
    list_of_exceptions = ["-", "'", " "]
    i = 0
    part_of_list = False
    corrupt_last_name = False
    newlastname = get_column(row, 2)
    last_name_length = len(newlastname)
    while i < last_name_length and corrupt_last_name == False:
        if newlastname[i] in list_of_exceptions:
            part_of_list = True
        else:
            pass
        i = i + 1
    if newlastname == None or newlastname == "":
        newlastname = newlastname
        corrupt_last_name = True
    elif last_name_length > 31:
        newlastname = truncate_string(newlastname, 30)
    elif newlastname.isalpha() == False and part_of_list == False :
        newlastname = newlastname
        corrupt_last_name = True

    return replace_column(row, newlastname, 2), corrupt_last_name
    


def check_score_coloumn(row,courruptscore):
    """Checks that the score coloumn has the correct parametres as well
    as calling the is_number module, which returns the score strings
    value as a float in boolean, as well as a digit integer data type,
    and that the  coloumn length is less than 7 characters 
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format
        courruptscore(BOOL): a boolean variable of the corrupt variable
    Return:
        str: Updated placing at indicated coloumn for each row of the score
        BOOL: returns a value of the scores validity to the parametres
    Preconditions:
        0<score_length<7
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        score_string is a none, "", digit, float

    """
    courruptscore = False
    score_string = get_column(row, 5)
    score_length = len(score_string)
    if score_length > 6:
        score_string = score_string
        courruptscore = True
    elif score_length <7 and score_string.isalpha() == True:
        score_string = score_string
        courruptscore = True
    elif score_string.isdigit() == True and score_length <7 :
        score_string = score_string
    elif is_number(score_string) == True and score_length <7:
        score_string = score_string
    elif score_string == None or score_string == "":
        score_string = score_string
    else:
        courruptscore = True
    
    return replace_column(row, score_string, 5),courruptscore
            



    
def check_time_module(row,corrupt_time):
    """Checks that the coloumns of the time, to coincide with
    the existing parametres, that is the time is less
    then 8 characters long, and is a float or intger
    data type, and return the validity of the check as well as the time value
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format
        corrupt_time(Boolean): Boolean value of the corrupt variable in main

    Return:
        row(str):  each row at indicated check
        Boolean: whether the parametres have been followed (True/False)
    Preconditions:
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        time_string is a digit or float, "" or None 
        corrupt_time = False
        

    """
    corrupt_time = False
    time_string = get_column(row, 6)
    time_string_length = len(time_string)
    if is_number(time_string) == True and time_string_length<9 :
        time_string = time_string
    elif time_string.isdigit() == True and time_string_length<9:
        time_string = time_string
    elif time_string == None or time_string == "":
        time_string = time_string
    elif time_string_length > 9:
        time_string = time_string
        corrupt_time = True
    elif is_number(time_string) == True and time_string_length <9:
        time_string = time_string
        corrupt_time = False
    else:
        time_string = time_string
        corrupt_time = True

    return replace_column(row,time_string, 6),corrupt_time


    
def is_number(s):
    """This function checks whether the data entered is a float, if not it
    handles an exception to the value error produced if not a float, returning
    a boolean value
    Parametres:
        s(float): Floating point value of the number'
    Return:
        Boolean: A true or false value for the entered number as a float
    Preconditions:
        S(number) is a float, string, None, "" or integer
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
                
   
   

def check_country_char(row, corruptedcountry):
    """Checks that the country coloumn has the correct parametres of 3
    letters that are uppercase and will check for
    that the  coloumn length is less than 3 characters. Will rectify country
    codes to a 3 character uppercase string
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated country code at indicated coloumn for each row
    Preconditions:
        0<country_length<4
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        Country is a none, "", string

    """
    corruptedcountry = False
    column_number = 3
    correct_country = False
    Country_String = get_column(row, 3)
    if len(Country_String) > 3:
        correct_country = False
        counrty = Country_String
        corruptedcountry = True
    elif Country_String == None or Country_String == "" :
        correct_country = False
        counrty =  Country_String
        corruptedcountry = True
    elif Country_String.isalpha() == False:
        correct_country = False
        counrty =  Country_String
        corruptedcountry = True
    else:
        correct_country = True

        
        

    if correct_country == True:
        counrty = Country_String.upper()
        

    return replace_column(row,counrty, 3), corruptedcountry

def check_six_seven_eight(row,corruptcolumns):
    """Checks that the coloumns six, seven and eight, coincide with
    the existing parametres, that is if six is a digit then either and not both
    coloumn seven and eight has a value, and return the validity of the check
    to write to the file. 
    Parametres :
        row(str): String of data in a CSV format
        corruptcolumns(Boolean): Boolean value of the corrupt variable in main

    Return:
        row(str):  each row at indicated check
        Boolean: whether the parametres have been followed (True/False)
    Preconditions:
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty
        Coloumn_six is a digit or other data type
        coloumn seven or eight are None, "", digit or Float

    """
    corruptcolumns = False
    coloumn_six = get_column(row, 4)
    coloun_seven = get_column(row, 5)
    coloumn_eight = get_column(row, 6)
    if coloumn_six.isdigit() == True:
        if coloun_seven != "" and coloumn_eight == "":
            corruptcolumns = False
        elif coloun_seven == "" and coloumn_eight != "":
            corruptcolumns = False
        else:
            corruptcolumns = True
            
    return row,corruptcolumns
   


    
def remove_athlete_id(row):
    """This function iterates over the variable 'i' using a syntax slice
    spliting the row from the , returning a new list with each coloumn
    of the row shifted 1 place to the left until the  while loop reaches the
    end of the coloumns for the row
    Parametres :
        row(str): String of data in a CSV format

    Return:
        str: Updated row without the athlete_ID coloumn for that record
    Preconditions:
        0<=i<=last_coloumn_in_row
        coloumn_number is >= 0  or <= last coloumn
        row <> Nothing or empty """
    i = 0
    while row[i] != ',' :
        i += 1
    return row[i+1:]

def main() :
    """Main functionality of program.Checks each function to return a value
    for the corrupt varibale, this increments the count if the check produces
    a corrupt return, if one coloumn is corrupt the entire reocrd is considered
    corrupt and written to the file"""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
         
        for row in raw_data_file :
            suffcient_data_is_entered = False
            corrupt = False
            corruptcountry = False
            corruptcount = 0
            row = remove_athlete_id(row)
            row,corrupt = check_medal(row,corrupt)
            row, corrupt = check_first_name(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt = check_country_char(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt = check_event_name(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt =  check_lastname(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt = check_time_module(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt = check_score_coloumn(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row,corrupt = check_place(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row, corrupt = check_six_seven_eight(row,corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            row, corrupt = check_coloumn_eleven_and_ten(row, corrupt)
            if corrupt == True:
                corruptcount = corruptcount + 1
            if corruptcount > 0:
                corrupt = True
            row_to_process = row
                    
            print(row_to_process)

            if not corrupt :
                clean_data_file.write(row_to_process)
                print("written")
            else :
                row = row[:-1]      # Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")    

# Call the main() function if this module is executed
if __name__ == "__main__" :
        main()
