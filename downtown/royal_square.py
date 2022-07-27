import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def royal_square():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = royal_square(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        royal_suite_min (dict)    - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)            - list of booleans whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite'''
    royal_suite_min = dict()
    is_vacant = ['No Info', 'No Info', 'No Info']
    suite_types = []
    rental_rates_min = []
    url = 'https://www.mainst.biz/apartments/edmonton/downtown-edmonton-apartments'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    suite_container = page_parsed.find('div', 'suites-container')
    suite_names = suite_container.findAll('span', 'bedrooms')
    suite_rates = suite_container.findAll('span', 'value')
    
    for name in suite_names:
        suite_types.append(name.text.strip())

    for rate in suite_rates:
        if rate.text.strip()[0] == '$':
            min_rate = rate.text.strip()[1:]
            if int(min_rate) > 699:
                rental_rates_min.append(min_rate)
    #print(rental_rates_min)

    for unit in suite_types:
        min_ = rental_rates_min.pop(0)
        royal_suite_min[unit] = min_

    #print(royal_suite_min, is_vacant)
    return royal_suite_min, is_vacant
    

if __name__ == '__main__':
    royal_square()