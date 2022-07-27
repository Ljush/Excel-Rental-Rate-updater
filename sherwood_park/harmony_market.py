import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def harmony_market():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.
    
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = harmony_market(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        harmony_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    harmony_suite_min = dict()
    #harmony_suite_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/harmony-at-the-market'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find span classes containing the names of the suite types
    for i in page_parsed.findAll('span', attrs={'class', 'suite-type title'}):
        suite_types.append(i.text.strip())

    # find span classes containing the rental rates for said suite types
    for j in page_parsed.findAll('span', 'value title'):
        rental_rates.append(j.text.strip()[1:])

    # find the <a> tags containing the 'Inquire' button
    # else covers the waiting list button if it is present. (wasn't present in rideau place)
    for v in page_parsed.findAll('a', 'open-suite-modal secondary-button'):
        if v.text.strip() == 'Inquire':
            is_vacant.append(True)
        else:
            is_vacant.append(False)
        
    # iterate thru suite_types and rental_rates to create the harmony_suite_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        harmony_suite_min[unit] = temp

    #print(harmony_suite_min, is_vacant)
    return harmony_suite_min, is_vacant
    
if __name__ == '__main__':
    harmony_market()