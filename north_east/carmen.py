import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def carmen():
    ''' Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = carmen(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        carm_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        carm_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    
    suite_types = [[], [], [], [], []]
    is_vacant = [[], [], [], [], []]
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/Carmen/'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the container for the suite_types
    temp_card_list = []
    section = page_parsed.find('section', 'multi-columns bottom-arrow')
    suite_cards = section.findAll('div', 'offer-card')
    
    # clean up each suite card for \n \r /MO and trailing whitespace, split into list per suite card
    for i in suite_cards:
        suite = i.text.strip()
        suite = suite.replace('\n', ' ')
        suite = suite.replace('\r', ' ')
        suite = suite.replace('/MO', '')
        unit_data = suite.split()
        temp_card_list.append(unit_data[:-3])
    

    card_list, is_vacant = get_vacancies(temp_card_list, is_vacant, suite_types)
    carm_suite_min, carm_suite_max = get_rates(card_list, suite_types)
    #print(carm_suite_min, carm_suite_max)
    return carm_suite_min, carm_suite_max, is_vacant

def get_rates(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    carm_suite_min = dict()
    carm_suite_max = dict()
    for i in temp_card_list:
        for j in i:
            if j[0] == '$':
                rate_string = j.replace('$', '')
                rate_string = rate_string.replace('-', ' ')
                rates = rate_string.split()
                # j might be deposit rate, len(rates) would be == 1 if so;
                if len(rates) == 2:
                    min_ = rates[0]
                    max_ = rates[1]
                    rental_rates_min.append(min_)
                    rental_rates_max.append(max_)
                    continue
    # build dictionaries of min/max rates and return them
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        carm_suite_min[unit] = min_rate
        carm_suite_max[unit] = max_rate
    #print(carm_suite_min, carm_suite_max)
    return carm_suite_min, carm_suite_max
        
def get_vacancies(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types (1 bed, 2 bed etc)"""
    card_list = [[], [], [], [], []]
    for j in temp_card_list:
        # 1 bedroom
        if j[0] == '1' and j[2] != '+':
            card_list[0] = j
            suite_types[0] = '1 Bedroom'
            if card_list[0][2].isdigit():
                is_vacant[0] = card_list[0][1]
            if card_list[0][2] == 'Available':
                is_vacant[0] = True
            if card_list[0][2] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 1 bed + den
        if j[0] == '1' and j[2] == '+':
            card_list[1] = j
            suite_types[1] = '1 Bedroom + Den'
            if card_list[1][4].isdigit():
                is_vacant[1] = card_list[1][4]
            if card_list[1][4] == 'Available':
                is_vacant[1] = True
            if card_list[1][4] == 'Waitlist':
                is_vacant[1] = False
            continue

        # 2 bedroom
        if j[0] == '2' and j[2] != '+':
            card_list[2] = j
            suite_types[2] = '2 Bedroom'
            if card_list[2][2].isdigit():
                is_vacant[2] = card_list[2][2]
            if card_list[2][2] == 'Available':
                is_vacant[2] = True
            if card_list[2][2] == 'Waitlist':
                is_vacant[2] = False
            continue

        # 2 bedroom + Den
        if j[0] == '2' and j[2] == '+':
            card_list[3] = j
            suite_types[3] = '2 Bedroom + Den'
            if card_list[3][4].isdigit():
                is_vacant[3] = card_list[3][4]
            if card_list[3][4] == 'Available':
                is_vacant[3] = True
            if card_list[3][4] == 'Waitlist':
                is_vacant[3] = False
            continue

        # 3 bedroom
        if j[0] == '3':
            card_list[4] = j
            suite_types[4] = '3 Bedroom'
            if card_list[4][2].isdigit():
                is_vacant[4] = card_list[5][3]
            if card_list[4][2] == 'Available':
                is_vacant[4] = True
            if card_list[4][2] == 'Waitlist':
                is_vacant[4] = False
            continue
    return card_list, is_vacant

if __name__ == '__main__':
    carmen()