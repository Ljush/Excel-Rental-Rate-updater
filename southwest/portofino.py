import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def portofino_suites():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = portofino_suites(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    
    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    portofino_suite_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '1 Bedroom, 2 Bath + Den', '2 Bedroom',
                   '2 Bedroom, 2 Bath', '2 Bedroom, 2 Bath + Den']
    rental_rates_min = []

    page = requests.get('https://www.portofinosuites.com/apartment-options')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rental rates
    for i in page_parsed.findAll('div', 'mar-t-2 co-cdk-fg'):
        temp = i.text[12] + i.text[14:17]
        rental_rates_min.append(temp)

    # website doesn't directly state available vacancies, will assume 'No Info'
    for j in range(len(suite_types)):
        is_vacant.append('No Info')

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        portofino_suite_min[unit] = temp_

    #print(portofino_suite_min, is_vacant)
    return portofino_suite_min, is_vacant

if __name__ == '__main__':
    portofino_suites()