# north_east_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def brintnell_landing():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = brintnell_landing(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    brintnell_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.brintnell-landing.ca/suites-and-amenities.php'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rental rates
    for i in page_parsed.findAll('div', 'unit-tile-price'):
        temp = i.text[12] + i.text[14:17]
        rental_rates_min.append(temp)

    # website doesn't directly state available vacancies, will assume 'No Info'
    for j in range(len(suite_types)):
        is_vacant.append('No Info')

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        brintnell_min[unit] = temp_

    #print(brintnell_min, is_vacant)
    return brintnell_min, is_vacant


def carmen():
    '''
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

    card_list, is_vacant = get_vacancies_carmen(
        temp_card_list, is_vacant, suite_types)
    carm_suite_min, carm_suite_max = get_rates_carmen(card_list, suite_types)
    #print(carm_suite_min, carm_suite_max)
    return carm_suite_min, carm_suite_max, is_vacant


def get_rates_carmen(temp_card_list, suite_types):
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


def get_vacancies_carmen(temp_card_list, is_vacant, suite_types):
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


def greenview():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = greenview(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    green_min = dict()
    #green_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.broadstreet.ca/residential/greenview'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('span', 'suite__name--text'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'suite__rate--text'):
        rental_rates_min.append(j.text[1:])

    # find suite vacancy status
    for k in page_parsed.findAll('span', 'suite__availability-text--text'):
        is_vacant.append(k.text[0])

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        green_min[unit] = rate

    #print(green_min, is_vacant)
    return green_min, is_vacant


def miller_ridge():
    """As of June 13th 2022, no suite cards are posted, only stating
    that 'Spacious apartments in edmonton' starting at $1080/month"""
    url = 'https://www.millerridge.ca/'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    suite_types = ['One Bedroom', 'One Bedroom+',
                   'Two Bedroom', 'Two Bedroom+']
    miller_min = dict()
    one_beds = ['One Bedroom', 'One Bedroom+']
    two_beds = ['Two Bedroom', 'Two Bedroom+']
    suite_list = []
    is_vacant = [False, False, False, False]

    # grab one/two bedroom cards from website
    section = page_parsed.findAll('div', 'content')
    for i in section:
        curr = i.text
        curr = curr.replace('\n', ' ')
        curr = curr.strip()
        curr = curr.split()
        suite_list.append(curr)

    # extract both "from $xx-$xx" values
    one_bed_rents = []
    two_bed_rents = []
    for j in suite_list:
        if j[0] == 'One':
            for k in j:
                if k[0] == '$':
                    one_bed_rents.append(k.replace('$', ''))
        if j[0] == 'Two':
            for k in j:
                if k[0] == '$':
                    two_bed_rents.append(k.replace('$', ''))

    single_dic = {}
    double_dic = {}
    for x in one_beds:
        if len(one_bed_rents) >= 1:
            rate = one_bed_rents.pop(0)
            single_dic[x] = rate
        else:
            single_dic[x] = '0'

    for y in two_beds:
        if len(two_bed_rents) >= 1:
            rate_ = two_bed_rents.pop(0)
            double_dic[y] = rate_
        else:
            double_dic[y] = '0'

    #print(single_dic, double_dic)

    for index, z in enumerate(suite_types):
        if index < 2:
            miller_min[z] = single_dic[z]
            if single_dic[z] != '0':
                is_vacant[index] = True
        if index >= 2:
            miller_min[z] = double_dic[z]
            if double_dic[z] != '0':
                is_vacant[index] = True

    #print(miller_min, is_vacant)
    return miller_min, is_vacant


def north_haven_estates():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = north_haven_estates(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        haven_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    haven_suite_min = dict()
    #haven_suite_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/north-haven-estates2'
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

    # iterate thru suite_types and rental_rates to create the haven_suite_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        haven_suite_min[unit] = temp

    #print(haven_suite_min, is_vacant)
    return haven_suite_min, is_vacant


def stella_place():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = stella_place(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    stella_min = dict()
    is_vacant = [False, False]
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = [[], []]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.stellaplace.ca/floorplans.aspx?web=1&wdLOR=cA9FBD4BD-1925-3941-8134-89F7F5BEB899'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    suite_card_list = []
    # grab data per suite card/type
    for i in page_parsed.findAll('div', 'span6'):
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\r', ' ')
        element = element.strip()
        element_list = element.split()
        if element_list == []:
            continue
        else:
            suite_card_list.append(element_list)

    # go thru data and extract rental rates/vacancy status
    """ Template of returning suite_card_list (June 13/2022)
['1', 'Bedroom', '(Contact', 'for', 'Availability)', 'Bed', '1', 'Bath', '1', 'Sq.Ft.648', 'Rent', 'Call', 'for', 'Details', 'Specials', 'Deposit', 'Contact', 'Us', '►']
['2', 'Bedroom', '(Available)', 'Bed', '2', 'Bath', '2', 'Sq.Ft.884', '-to', '934', 'Rent', '$1,500', 'Specials', 'Deposit', 'Available', '►']"""
    temp_rents = [[], []]
    for j in suite_card_list:
        #print(j)
        # 1 bedroom
        if j[0] == '1':
            if 'Call' in j:
                temp_rents[0] = '0'
            else:
                temp_rents[0] = j[11]
                is_vacant[0] = True

        # 2 bedroom
        if j[0] == '2':
            if 'Call' in j:
                temp_rents[1] = 0
            else:
                temp_rents[1] = j[11]
                is_vacant[1] = True

    # remove commas from rental rates;
    for index, m in enumerate(temp_rents):
        rent = m
        rent = rent.replace(',', '')
        rent = rent.replace('$', '')
        rental_rates_min[index] = rent

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        stella_min[unit] = rate

    #print(stella_min, is_vacant)
    return stella_min, is_vacant


def wyndham_crossing():
    wynd_suite_min = dict()
    suite_types = ['maple', 'willow', 'cotton', 'pine']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/wyndham-crossing/floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    wynd_scripts = page_parsed.findAll('div', 'accordion-inner')
    for i in wynd_scripts:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', '')
        element = element.strip()
        print(repr(element))

    # isolate script 64 and cut out large parts of the str(script)
    # script = wynd_scripts[63].text[292:-1500]
    # script = script.replace("\n", "")
    # script = script.replace('\t', '')
    # script = script.replace('\r', '')
    # script = script.strip()
    # # since script is extremely long string, split it per '}' into list
    # script_list = script.split('}')
    return
    #print(wynd_suite_min, is_vacant_final)
    #return wynd_suite_min, is_vacant_final


if __name__ == '__main__':
    pass
