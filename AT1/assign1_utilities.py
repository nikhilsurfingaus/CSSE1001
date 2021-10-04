"""
Support file for Olympic results data cleaning (Assignment 1) in CSSE1001.

Reads the athlete data from the raw data text file.
Data is read and returned one line of the file at a time.
Reading starts from the beginning of the file and continues until the end of
the file.

Writes the processed data to the cleaned data file.
Date is written one line at a time.
"""

__author__ = "Richard Thomas"
__date__ = "15/02/2018"
__copyright__ = "The University of Queensland, 2018"



def get_column(row, column_number) :
    """Return a string containing the data at the indicated column in the row.

    Parameters:
        row (str): String of data with comma separators (CSV format).
        column_number (int): Index of the data to be returned.

    Return:
        str: Data at 'column_number' position in 'row'

    Preconditions:
        row != None
        0 <= column_number <= maximum number of columns in 'row'
    """
    row_data = row.split(',')
    return row_data[column_number]



def replace_column(row, data, column_number) :
    """Replace the data at the indicated column in the row.

    Parameters:
        row (str): String of data with comma separators (CSV format).
        data (str): Text to replace the data at the indicated column.
        column_number (int): Index of the data to be replaced.

    Return:
        str: Updated row with 'data' in the indicated column.

    Preconditions:
        row != None and data != None
        0 <= column_number <= maximum number of columns in 'row'
    """
    row_data = row.split(',')
    row_data[column_number] = data

    # Create resulting string with updated data in column_number
    resulting_row = ""
    for column_data in row_data :
        resulting_row += column_data + ","    # Add comma between each column
    return resulting_row[:-1]           # Remove extra comma at end of string



def truncate_string(string_to_truncate, max_length) :
    """Returns a string up to 'max_length' characters in size.

    Parameters:
        string_to_truncate (str): String to be truncated.
        max_length (int): Maximum length of returned string.

    Returns:
        str: Characters 0 to max_length-1 (or end of string) from
             string_to_truncate.

    Preconditions:
        len(string_to_truncate) >= 0
        max_length >= 0
    """
    return string_to_truncate[:max_length]



# Check if an attempt is made to execute this module and output error message
if __name__ == "__main__" :
    print("This module provides utility functions for reading data from the",
          "Olympic results file and is not meant to be executed on its own.")
