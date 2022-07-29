# Datetime checker
#from calendar import month
from datetime import datetime
'''
Datetime module documentation
https://docs.python.org/3/library/datetime.html
'''
def find_current_month():
    """get the current time and date, changing the date to the first day of the current month"""
    month_dictionary = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                        5: 'May', 6: 'June', 7: 'July', 8: 'August',
                        9: 'September', 10: 'October', 11: 'November',
                        12: 'December'}
    date_today = datetime.now()
   # month_first_day = date_today.replace(
        #day=1, hour=0, minute=0, second=0, microsecond=0)
    month_ = date_today.timetuple()
    return date_today, month_[1], month_[0], month_dictionary, date_today

if __name__ == '__main__':
    find_current_month()