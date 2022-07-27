import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def cornerstone_callaghan():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE
    1 - right click -> Run Current File in Interactive Window
    2 - paste -> >  d, x = cornerstone_callaghan()
    print('Rental rates:', d, '\nVacancies:', x)
    3 - run the code to visualize what the dictionary of units and list of
    vacancy bools(is_vacant)
    
    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    cornerstone_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    page = requests.get(
        'https://www.broadstreet.ca/residential/cornerstone-at-callaghan')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite names
    for i in page_parsed.findAll('span', 'suite__name--text'):
        suite_types.append(i.text)
    #print(suite_types)

    # grab rental rates per suite
    for j in page_parsed.findAll('span', 'suite__rate--text'):
        rental_rates_min.append(j.text[1:])
    #print(rental_rates_min)

    # grab availability of suites (vacancies)
    for k in page_parsed.findAll('span', 'suite__availability-text--text'):
        is_vacant.append(k.text[0])
    #print(is_vacant)

    for unit in suite_types:
        temp = rental_rates_min.pop(0)
        cornerstone_suite_min[unit] = temp

    #print(cornerstone_suite_min, is_vacant)
    return cornerstone_suite_min, is_vacant

if __name__ == '__main__':
    cornerstone_callaghan()