import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def rideau_place():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = rideau_place(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)

    Vars:
        No max rates for rideau place right now!
        rideau_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)        - list of booleans whether the unit has vacancy or not
        suite_types (list)      - 1 bed, 2 bed, 3 bed etc. as of may 10/2022 
                                  3 beds are not listed on the site but i think 
                                  this script would manage its appearance just fine.
        suite_rental_rates(list)- '$xxx' rental rates per suite'''
    rideau_suite_min = dict()
    #rideau_suite_max = dict()
    is_vacant = []
    suite_types = []
    suite_rental_rates = []
    # grab the rideau place URL and parse it with beautifulsoup
    page = requests.get('https://www.mmgltd.com/apartment-rentals/rideau-place')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find span classes containing the names of the suite types
    for i in page_parsed.findAll('span', attrs={'class', 'suite-type title'}):
        suite_types.append(i.text.strip())

    # find span classes containing the rental rates for said suite types
    for j in page_parsed.findAll('span', 'value title'):
        suite_rental_rates.append(j.text.strip()[1:])

    # find the <a> tags containing the 'Inquire' button, we can assume anything 
    # else would not have any vacancies
    for v in page_parsed.findAll('a', 'open-suite-modal secondary-button'):
        if v.text.strip() == 'Inquire':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    # iterate thru suite_types and suite_rental_rates to create the rideau_suite_min dictionary
    for unit in suite_types:
        _rate = suite_rental_rates.pop(0)
        rideau_suite_min[unit] = _rate

    #print(rideau_suite_min, is_vacant)
    return rideau_suite_min, is_vacant

if __name__ == '__main__':
    rideau_place()