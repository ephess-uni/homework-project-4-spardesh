# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    # Initialize an empty list to store reformatted dates
    dates = []
    
    # Iterate through each date string in the input list
    for date_str in old_dates:
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Format the datetime object as 'dd Mon YYYY' and append to the list
        formatted_date = date_obj.strftime('%d %b %Y')
        dates.append(formatted_date)
    
    return dates  # Return the list of reformatted dates


def date_range(start, n):
    # Check if 'start' is a string
    if not isinstance(start, str):
        raise TypeError("start should be a string")
    
    # Check if 'n' is an integer
    if not isinstance(n, int):
        raise TypeError("n should be an integer")
    
    # Convert the start date string to a datetime object
    date = datetime.strptime(start, '%Y-%m-%d')
    
    # Generate a list of datetime objects for the specified range of days
    date_list = [date + timedelta(days=i) for i in range(n)]
    
    return date_list  # Return the list of datetime objects


def add_date_range(values, start_date):
    # Generate a date range using the 'date_range' function
    obj = date_range(start_date, len(values))
    
    # Combine the date range with the input values into a list of tuples
    result = [(date, value) for date, value in zip(obj, values)]
    
    return result  # Return the list of tuples


def fees_report(infile, outfile):
    # Initialize a defaultdict to store late fees for each patron
    late_fees = defaultdict(float)
    
    # Initialize a set to keep track of all unique patrons
    all_patrons = set() 
    
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            # Convert date strings to datetime objects
            checkout_date = datetime.strptime(row['date_checkout'], '%m/%d/%Y')
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            returned_date = datetime.strptime(row['date_returned'], '%m/%d/%Y')  # Adjust date format
            
            if returned_date > due_date:
                # Calculate late fees for each patron
                days_late = (returned_date - due_date).days
                late_fees[row['patron_id']] += days_late * 0.25
            
            # Add patron to the set of all patrons
            all_patrons.add(row['patron_id'])  
    
    for patron_id in all_patrons:
        if patron_id not in late_fees:
            # Initialize late fees to 0 for patrons with no late returns
            late_fees[patron_id] = 0.0
    
    with open(outfile, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            # Write patron ID and late fees to the output file
            writer.writerow({'patron_id': patron_id, 'late_fees': f'{fee:.2f}'})



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
