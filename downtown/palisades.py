import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def palisades():
    ''' Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = palisades(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        pali_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        pali_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    
    suite_types = ['Bachelor', 'Bachelor Premium', 'One Bedroom',
                   'One Bedroom Premium', 'Two Bedroom', 'Two Bedroom Premium']
    is_vacant = [False, False, False, False, False, False]
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/the-palisades/'
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


    """ ===>> Template of what the lists look like after being split, since they develope in the order left to right on the website
    ['Bachelor', 'Available', '$777-$1119', 'Bathrooms:1', 'Sq', 'Ft:450', 'Deposit:', '$299', 'Book', 'a', 'Viewing']
    ['1', 'Bedroom', 'Available', '$862-$1269', 'Bathrooms:1', 'Sq', 'Ft:850', 'Deposit:', '$299', 'Book', 'a', 'Viewing']
    ['Bachelor', 'Premium', 'Available', '$854-$1169', 'Bathrooms:1', 'Sq', 'Ft:450', 'Deposit:', '$299', 'Book', 'a', 'Viewing']
    ['2', 'Bedroom', '1', 'Suite', 'Left', '$1439-$1569', 'Bathrooms:1', 'Sq', 'Ft:1164', 'Deposit:', '$299', 'Book', 'a', 'Viewing']
    ['1', 'Bedroom', 'Premium', 'Waitlist', '$1239-$1319', 'Bathrooms:1', 'Sq', 'Ft:850', 'Deposit:', '$299', 'Waitlist']
    ['2', 'Bedroom', 'Premium', 'Waitlist', '$1529-$1619', 'Bathrooms:1', 'Sq', 'Ft:1164', 'Deposit:', '$299', 'Waitlist']
    ['2', 'Bedroom', 'Penthouse', 'Waitlist', '$1739-$1789', 'Bathrooms:1.5', 'Sq', 'Ft:1300', 'Deposit:', '$299', 'Waitlist']
    ['3', 'Bedroom', 'Penthouse', 'Waitlist', '$1689-$1789', 'Bathrooms:1.5', 'Sq', 'Ft:1300', 'Deposit:', '$299', 'Waitlist']
    ['3', 'Bedroom', 'Penthouse', 'Premium', 'Waitlist', '$1789-$1839', 'Bathrooms:1.5', 'Sq', 'Ft:1300', 'Deposit:', '$299', 'Waitlist']"""
    
    """Doesn't include 3 bedrooms since they are not currently collected on the spreadsheet;
    Could possibly break if sq ft of suite changes?? """

    card_list, is_vacant = get_vacancies(temp_card_list, is_vacant, suite_types)
    pali_suite_min, pali_suite_max = get_rates(card_list, suite_types)
    #print(pali_suite_min); print(pali_suite_max); print(is_vacant)
    return pali_suite_min, pali_suite_max, is_vacant

def get_rates(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    pali_suite_min = dict()
    pali_suite_max = dict()
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
        pali_suite_min[unit] = min_rate
        pali_suite_max[unit] = max_rate

    return pali_suite_min, pali_suite_max
        
def get_vacancies(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types (1 bed, 2 bed etc)"""
    card_list = [[], [], [], [], [], []]
    for j in temp_card_list:
        # bachelor
        if j[0] == 'Bachelor' and j[1] != 'Premium':
            card_list[0] = j
            suite_types[0] = card_list[0][0]
            if card_list[0][1].isdigit():
                is_vacant[0] = card_list[0][1]
            if card_list[0][1] == 'Available':
                is_vacant[0] = True
            if card_list[0][1] == 'Waitlist':
                is_vacant[0] = False
            continue

        # bachelor premium
        if j[0] == 'Bachelor' and j[1] == 'Premium':
            card_list[1] = j
            suite_types[1] = card_list[1][0] + ' Premium'
            if card_list[1][2].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][2] == 'Available':
                is_vacant[1] = True
            if card_list[1][2] == 'Waitlist':
                is_vacant[1] = False
            continue

        # 1 bedroom
        if j[0] == '1' and j[2] != 'Premium':
            card_list[2] = j
            suite_types[2] = card_list[2][0] + f' {card_list[2][1]}'
            if card_list[2][2].isdigit():
                is_vacant[2] = card_list[2][2]
            if card_list[2][2] == 'Available':
                is_vacant[2] = True
            if card_list[2][2] == 'Waitlist':
                is_vacant[2] = False
            continue

        # 1 bedroom premium
        if j[0] == '1' and j[2] == 'Premium':
            card_list[3] = j
            suite_types[3] = card_list[3][0] + f' {card_list[3][1]} Premium'
            if card_list[3][3].isdigit():
                is_vacant[3] = card_list[3][3]
            if card_list[3][3] == 'Available':
                is_vacant[3] = True
            if card_list[3][3] == 'Waitlist':
                is_vacant[3] = False
            continue

        # 2 bedroom premium
        if j[0] == '2' and j[2] == 'Premium':
            card_list[5] = j
            suite_types[5] = card_list[5][0] + f' {card_list[5][1]} Premium'
            if card_list[5][3].isdigit():
                is_vacant[5] = card_list[5][3]
            if card_list[5][3] == 'Available':
                is_vacant[5] = True
            if card_list[5][3] == 'Waitlist':
                is_vacant[5] = False
            continue

        # 2 bedroom
        if j[0] == '2' and j[2] != 'Premium' and j[2] != 'Penthouse':
            card_list[4] = j
            suite_types[4] = card_list[4][0] + f' {card_list[4][1]}'
            if card_list[4][2].isdigit():
                is_vacant[4] = card_list[4][2]
            if card_list[4][2] == 'Available':
                is_vacant[4] = True
            if card_list[4][2] == 'Waitlist':
                is_vacant[4] = False
            continue
    return card_list, is_vacant

if __name__ == '__main__':
    palisades()