import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def secord_house():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = secord_house(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/secord-house/floorplans.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

if __name__ == '__main__':
    secord_house()