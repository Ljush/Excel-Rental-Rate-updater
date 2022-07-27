import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def wellington_court():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    wellington_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    sq_ft_variations = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/wellington-court-apartments/floorplans.aspx'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab variation titles
    wellington_data = page_parsed.findAll('div', 'accordion-inner')
    for i in wellington_data:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.strip()
        element = element.split()
        print(repr(element))
        
    

if __name__ == '__main__':
    wellington_court()