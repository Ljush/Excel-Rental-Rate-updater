import requests
from tkinter import Tk, filedialog
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def avalon_downtown():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = avalon_downtown(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/avalon-apartments-0/floorplans.aspx/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    root = Tk()
    root.withdraw()
    open_file = filedialog.askopenfilename()
    print('')
    print(repr(open_file))
    print('\n')
    print(open_file)



if __name__ == '__main__':
    avalon_downtown()