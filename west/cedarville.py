import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def cedarville():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = cedarville(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for cedarville right now!
        cedarville_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        cedarville_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], []]
    suite_types = [[], []]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/cedarville-apartments/'
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
    cedarville_min, cedarville_max = get_rates(card_list, suite_types)
    #print(cedarville_min, cedarville_max); print(is_vacant)
    return cedarville_min, cedarville_max, is_vacant


def get_vacancies(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], []]
    for i in temp_card_list:
        # 2 bedroom
        if i[0] == '2' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[0] = i
            suite_types[0] = i[0] + f' {i[1]}'
            if card_list[0][2].isdigit():
                is_vacant[0] = card_list[0][2]
            if card_list[0][2] == 'Available':
                is_vacant[0] = True
            if card_list[0][2] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 2 bedroom premium
        if i[0] == '2' and i[2] == 'Premium':
            card_list[1] = i
            suite_types[1] = i[0] + f' {i[1]} Premium'
            if card_list[1][3].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][3] == 'Available':
                is_vacant[1] = True
            if card_list[1][3] == 'Waitlist':
                is_vacant[1] = False
            continue
    return card_list, is_vacant

def get_rates(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    cedarville_min = dict()
    cedarville_max = dict()
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
        cedarville_min[unit] = min_rate
        cedarville_max[unit] = max_rate
    return cedarville_min, cedarville_max

if __name__ == '__main__':
    cedarville()