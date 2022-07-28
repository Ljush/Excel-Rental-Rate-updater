#downtown_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def park_square():
    park_suite_min = dict()
    is_vacant = []
    # no names given per suite type, sqft shouldn't change (?)
    suite_types = ['850 sqft', '960 sqft', '1050 sqft']
    rental_rates_min = []
    url = 'https://www.quadrealres.com/apartments/ab/edmonton/park-square-6/floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    park_scripts = page_parsed.findAll('script')
    # isolate script 62 that contains information for each suite card on the website
    script = park_scripts[61].text[292:-1500]
    script = script.replace('\n', '')
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    script_list = script.split('}')

    # two bedroom -> 850 sqft (small)
    small = script_list[0]
    small = small[148:-230]
    small = small.split()
    #print(small)

    # two bedroom -> 960 sqft (medium)
    medium = script_list[2]
    medium = medium[150:-230]
    medium = medium.split()
    #print('\n', medium)

    # two bedroom -> 1050 sqft (large)
    large = script_list[4]
    large = large[155:-40]
    large = large.split()
    #print('\n', large)

    # order rental rates + vacancy status/numbers according to the spreadsheet
    temp_rates = [small[5], medium[5], large[5]]
    #print(temp_rates)

    # remove floating zeroes, commas, and dollar signs from the list elements (str)
    for i in temp_rates:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        rental_rates_min.append(i)
    """
    # remove commas from vacancy status
    temp_vacancy = [small[7], medium[7], large[7]]
    for j in temp_vacancy:
        j = j.replace(',', '')
        is_vacant.append(j)
    """

    """July 26/2022 - studio + 2b + 2b + 2b
        [497 sqft, 850 sqft, 960 sqft, 1050 sqft] """
    for x in rental_rates_min:
        if x == 0:
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    # build rental rate dictionary
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        park_suite_min[unit] = rate

    #print(park_suite_min, is_vacant)
    return park_suite_min, is_vacant

def hi_level_place():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = hi_level_place(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    level_min_rates = dict()
    suite_types = ['Bachelor', 'Bachelor Renovated', 'One Bedroom',
                   'One Bedroom Renovated', 'Two Bedroom',
                   'Two Bedroom Renovated']
    url = 'https://www.minto.com/edmonton/Edmonton-apartment-rentals/Hi-Level-Place/main.html#rates_floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    table = page_parsed.find(
        'table', 'table table-striped__ table-responsive-minto border-bottom')
    site_data = table.findAll('tr', 'text-center py-3 py-md-0')
    #print(repr(site_data[2].text))
    temp_data_list = []
    for j in site_data:
        data = j.text
        #print(repr(data))
        data = data.replace('\n', ' ')
        data = data.strip()
        temp_name_list = data.split()
        temp_name_list = temp_name_list[:-3]
        #print(temp_name_list)
        temp_data_list.append(temp_name_list)

    rental_rates_min, is_vacant = get_rates(temp_data_list)

    #print(rental_rates_min, is_vacant)
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        if min_rate == []:
            level_min_rates[unit] = '0'
        else:
            level_min_rates[unit] = min_rate

    #print(level_min_rates, is_vacant)
    return level_min_rates, is_vacant


def mountbatten():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = mountbatten(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    mount_min_rates = dict()
    mount_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info']
    suite_types = ['Bachelor', 'Bachelor Elite', '1 Bedroom', '2 Bedroom']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://greatapartments.ca/mha_property/the-mountbatten/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    rate_info = page_parsed.findAll('div', 'mb-3')
    temp_rate_list = []
    for g in rate_info:
        if len(temp_rate_list) >= 4:
            break
        rate = g.text
        rate = rate.replace('\n', '')
        rate = rate.strip()

        # take only rent rate texts; that are also not deposits
        if rate[0] == '$' and rate[-1] != 't':
            temp_rate_list.append(rate)

    #print(temp_rate_list)
    for i in temp_rate_list:
        rent_rate = i
        rent_rate = rent_rate.replace('$', '')
        rent_rate = rent_rate.replace('-', ' ')
        rent_rate = rent_rate.replace(' /mo.', '')
        rent_rate = rent_rate.replace(',', '')

        rent_temp_list = rent_rate.split()
        min_rate = rent_temp_list[0]
        max_rate = rent_temp_list[1]
        rental_rates_min.append(min_rate)
        rental_rates_max.append(max_rate)

    """Vacancy status is unknown, comment on the availability column
        that only "Book a viewing" is showing per suite type"""

    for unit in suite_types:
        min_ = rental_rates_min.pop(0)
        max_ = rental_rates_max.pop(0)
        mount_min_rates[unit] = min_
        mount_max_rates[unit] = max_

    #print(mount_min_rates, mount_max_rates, is_vacant)
    return mount_min_rates, mount_max_rates, is_vacant


def le_jardin():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = le_jardin(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    jardin_min_rates = dict()
    jardin_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info']
    suite_types = ['1 Bedroom', '1 Bedroom Elite', '1 Bedroom Luxury Elite']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://greatapartments.ca/mha_property/le-jardin/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    rate_info = page_parsed.findAll('div', 'mb-3')
    temp_rate_list = []
    for g in rate_info:
        if len(temp_rate_list) >= 4:
            break
        rate = g.text
        rate = rate.replace('\n', '')
        rate = rate.strip()

        # take only rent rate texts; that are also not deposits
        if rate[0] == '$' and rate[-1] != 't':
            temp_rate_list.append(rate)
        # "Check back soon" when no rate posted
        if rate[0] == 'C':
            temp_rate_list.append('$0-$0')

    #print(temp_rate_list)

    for i in temp_rate_list:
        rent_rate = i
        rent_rate = rent_rate.replace('$', '')
        rent_rate = rent_rate.replace('-', ' ')
        rent_rate = rent_rate.replace(' /mo.', '')
        rent_rate = rent_rate.replace(',', '')

        rent_temp_list = rent_rate.split()
        min_rate = rent_temp_list[0]
        max_rate = rent_temp_list[1]
        rental_rates_min.append(min_rate)
        rental_rates_max.append(max_rate)

    # temporarily reorder these rates according to their order on the website; monitor this
    reordered_min_rates = [rental_rates_min[2], rental_rates_min[1],
                           rental_rates_min[0]]
    reordered_max_rates = [rental_rates_max[2], rental_rates_max[1],
                           rental_rates_max[0]]

    """Vacancy status is unknown, comment on the availability column
        that only "Book a viewing" is showing per suite type"""

    for unit in suite_types:
        min_ = rental_rates_min.pop(0)
        max_ = rental_rates_max.pop(0)
        jardin_min_rates[unit] = min_
        jardin_max_rates[unit] = max_

    #print(jardin_min_rates, jardin_max_rates, is_vacant)
    return jardin_min_rates, jardin_max_rates, is_vacant


def avalon_downtown():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = avalon_downtown(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/avalon-apartments-0/floorplans.aspx/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    return


def secord_house():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = secord_house(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/secord-house/floorplans.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')


def valley_ridge():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = valley_ridge(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        valley_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        valley_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    suite_types = [[], [], [], [], []]
    is_vacant = [[], [], [], [], []]
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/valley-ridge-tower/'
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

    card_list, is_vacant = get_vacancies_valley(
        temp_card_list, is_vacant, suite_types)
    valley_suite_min, valley_suite_max = get_rates_valley(
        card_list, suite_types)
    #print(valley_suite_min, valley_suite_max)
    return valley_suite_min, valley_suite_max, is_vacant


def palisades():
    '''
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

    card_list, is_vacant = get_vacancies_palisades(
        temp_card_list, is_vacant, suite_types)
    pali_suite_min, pali_suite_max = get_rates_palisades(
        card_list, suite_types)
    #print(pali_suite_min); print(pali_suite_max); print(is_vacant)
    return pali_suite_min, pali_suite_max, is_vacant


def get_rates_palisades(temp_card_list, suite_types):
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


def maureen_manor():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = maureen_manor(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        maureen_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        maureen_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.'''
    is_vacant = [[], [], [], []]
    suite_types = [[], [], [], []]
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/maureen-manor/'
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

    card_list, is_vacant = get_vacancies_maureen(
        temp_card_list, is_vacant, suite_types)
    maureen_min, maureen_max = get_rates_maureen(card_list, suite_types)
    #print(maureen_min, maureen_max); print(is_vacant)
    return maureen_min, maureen_max, is_vacant


def get_vacancies_maureen(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], [], []]
    for i in temp_card_list:
        # 1 bedroom
        if i[0] == '1' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[0] = i
            suite_types[0] = i[0] + f' {i[1]}'
            if card_list[0][2].isdigit():
                is_vacant[0] = card_list[0][2]
            if card_list[0][2] == 'Available':
                is_vacant[0] = True
            if card_list[0][2] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 1 bedroom premium
        if i[0] == '1' and i[2] == 'Premium':
            card_list[1] = i
            suite_types[1] = i[0] + f' {i[1]} Premium'
            if card_list[1][3].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][3] == 'Available':
                is_vacant[1] = True
            if card_list[1][3] == 'Waitlist':
                is_vacant[1] = False
            continue

        # 2 bedroom
        if i[0] == '2' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[2] = i
            suite_types[2] = i[0] + f' {i[1]}'
            if card_list[2][2].isdigit():
                is_vacant[2] = card_list[2][2]
            if card_list[2][2] == 'Available':
                is_vacant[2] = True
            if card_list[2][2] == 'Waitlist':
                is_vacant[2] = False
            continue

        # 2 bedroom premium
        if i[0] == '2' and i[2] == 'Premium':
            card_list[3] = i
            suite_types[3] = i[0] + f' {i[1]} Premium'
            if card_list[3][3].isdigit():
                is_vacant[3] = card_list[3][2]
            if card_list[3][3] == 'Available':
                is_vacant[3] = True
            if card_list[3][3] == 'Waitlist':
                is_vacant[3] = False
            continue
    return card_list, is_vacant


def residence():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = residence(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        residence_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    residence_suite_min = dict()
    #residence_suite_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/the-residence'
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

    # iterate thru suite_types and rental_rates to create the residence_suite_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        residence_suite_min[unit] = temp

    #print(residence_suite_min, is_vacant)
    return residence_suite_min, is_vacant

def royal_square():
    '''
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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

def get_rates_maureen(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    maureen_min = dict()
    maureen_max = dict()
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
        maureen_min[unit] = min_rate
        maureen_max[unit] = max_rate
    return maureen_min, maureen_max


def rossdale():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = rossdale(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        rossdale_suite_min (dict)    - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)            - list of booleans whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite'''
    rossdale_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    # midwest has updated cloudflare to flag botting? we use navigation.useragent >>(headers)
    # data from the midwest village website to bypass the '403 forbidden' error to bypass this lol
    url = 'https://rentmidwest.com/location/rossdale-house-edmonton-apartment-rental/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    suite_names_parsed = page_parsed.find('div', 'property-types')
    details_1 = suite_names_parsed.find_all('div', 'details-1')
    details_2 = suite_names_parsed.find_all('div', 'details-2')
    for i in details_1:
        str_temp = i.text.replace('\t', '')
        str_temp = str_temp.replace('\n', '')

        if int(str_temp[0:4]):
            suite_types.append(str(str_temp[0:4].strip()))
            continue
        else:
            suite_types.append(str_temp)

    # since we are using the sqft measurements to signify what type of unit it is
    # we add a '_2' to the last list element to distinguish the 1 bed from the 2 bed of the same size
    suite_types[-1] = f'{suite_types[-1]} 2_Bed'

    for j in details_2:
        rate_temp = j.text.replace('\n', '')
        rate = rate_temp[12:-3]
        rental_rates_min.append(rate)
    #print(rental_rates_min)

    for unit in suite_types:
        rent_rate = rental_rates_min.pop(0)
        rossdale_suite_min[unit] = rent_rate

    for vacancy in range(len(suite_types)):
        is_vacant.append('Waitlist')

    '''same deal with The village on Southwest sheet, no info is given so we can assume 
    that a waitlist is their default because they seem to push the user to submit an application
    or call to check if they can apply/have vacancies'''

    #print(rossdale_suite_min, is_vacant)
    return rossdale_suite_min, is_vacant

def get_vacancies_palisades(temp_card_list, is_vacant, suite_types):
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

def get_rates_valley(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    valley_suite_min = dict()
    valley_suite_max = dict()
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
        valley_suite_min[unit] = min_rate
        valley_suite_max[unit] = max_rate
    return valley_suite_min, valley_suite_max


def get_vacancies_valley(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], [], [], []]
    for i in temp_card_list:
        # bachelor
        if i[0] == 'Bachelor' and i[5] == 'Ft:311':
            card_list[0] = i
            suite_types[0] = i[0]
            if card_list[0][1].isdigit():
                is_vacant[0] = card_list[0][1]
            if card_list[0][1] == 'Available':
                is_vacant[0] = True
            if card_list[0][1] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 1 bedroom
        if i[0] == '1' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[1] = i
            suite_types[1] = i[0] + f' {i[1]}'
            if card_list[1][2].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][2] == 'Available':
                is_vacant[1] = True
            if card_list[1][2] == 'Waitlist':
                is_vacant[1] = False
            continue

        # 1 bedroom premium
        if i[0] == '1' and i[2] == 'Premium':
            card_list[2] = i
            suite_types[2] = i[0] + f' {i[1]} Premium'
            if card_list[2][3].isdigit():
                is_vacant[2] = card_list[2][2]
            if card_list[2][3] == 'Available':
                is_vacant[2] = True
            if card_list[2][3] == 'Waitlist':
                is_vacant[2] = False
            continue

        # 2 bedroom
        if i[0] == '2' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[3] = i
            suite_types[3] = i[0] + f' {i[1]}'
            if card_list[3][2].isdigit():
                is_vacant[3] = card_list[3][2]
            if card_list[3][2] == 'Available':
                is_vacant[3] = True
            if card_list[3][2] == 'Waitlist':
                is_vacant[3] = False
            continue

        # 2 bedroom premium
        if i[0] == '2' and i[2] == 'Premium':
            card_list[4] = i
            suite_types[4] = i[0] + f' {i[1]} Premium'
            if card_list[4][3].isdigit():
                is_vacant[4] = card_list[4][2]
            if card_list[4][3] == 'Available':
                is_vacant[4] = True
            if card_list[4][3] == 'Waitlist':
                is_vacant[4] = False
            continue
    return card_list, is_vacant

def get_rates(temp_data_list):
    is_vacant = [False, False, False, False, False, False]
    rental_rates_min = [[], [], [], [], [], []]
    suite_data_list = [[], [], [], [], [], []]

    for w in temp_data_list:
        #print(w)
        # Bachelor unit
        if w[0] == 'Bachelor' and w[1] != 'Renovated':
            suite_data_list[0] = w
            # determine if the bachelor has vacancy or not
            if 'Available' in suite_data_list[0]:
                is_vacant[0] = True
            if 'Waitlist' in suite_data_list[0]:
                is_vacant[0] = False

            # grab the rate of the bachelor suite
            for element in suite_data_list[0]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[0] = rate
            if rental_rates_min[0] == []:
                rental_rates_min[0] = '0'

        # renovated bachelor unit
        if w[0] == 'Bachelor' and w[1] == 'Renovated':
            suite_data_list[1] = w

            # determine the vacancy of the renovated bachelor suites
            if 'Available' in suite_data_list[1]:
                is_vacant[1] = True
            if 'Waitlist' in suite_data_list[1]:
                is_vacant[1] = False

            # determine the rate of the renovated bachelor suites
            for element in suite_data_list[1]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[1] = rate
            if rental_rates_min[1] == []:
                rental_rates_min[1] = '0'

        # one bedroom
        if w[0] == 'One' and w[1] == 'Bedroom' and w[2] != 'Renovated':
            suite_data_list[2] = w

            # determine if the one bedroom suites have vacancy
            if 'Available' in suite_data_list[2]:
                is_vacant[2] = True
            if 'Waitlist' in suite_data_list[2]:
                is_vacant[2] = False

            # determine the starting rate for the one bedroom suites
            for element in suite_data_list[2]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[2] = rate
            if rental_rates_min[2] == []:
                rental_rates_min[2] = '0'

        if w[0] == 'One' and w[1] == 'Bedroom' and w[2] == 'Renovated':
            suite_data_list[3] = w

            # determine if the renovated one bedroom suites have vacancy
            if 'Available' in suite_data_list[3]:
                is_vacant[3] = True
            if 'Waitlist' in suite_data_list[3]:
                is_vacant[3] = False

            # determine the starting rate for the renovated one bedroom suites
            for element in suite_data_list[3]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[3] = rate
            if rental_rates_min[3] == []:
                rental_rates_min[3] = '0'

        # two bedroom
        if w[0] == 'Two' and w[1] == 'Bedroom' and w[2] != 'Renovated':
            suite_data_list[4] = w

            # determine if the  two bedroom suites have vacancy
            if 'Available' in suite_data_list[4]:
                is_vacant[4] = True
            if 'Waitlist' in suite_data_list[4]:
                is_vacant[4] = False

            # determine the starting rate for the two bedroom suites
            for element in suite_data_list[4]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[4] = rate
            if rental_rates_min[4] == []:
                rental_rates_min[4] = '0'

        # two bedroom renovated
        if w[0] == 'Two' and w[1] == 'Bedroom' and w[2] == 'Renovated':
            suite_data_list[5] = w

            # determine if the renovated two bedroom suites have vacancy
            if 'Available' in suite_data_list[5]:
                is_vacant[5] = True
            if 'Waitlist' in suite_data_list[5]:
                is_vacant[5] = False

            # determine the starting rate for the renovated two bedroom suites
            for element in suite_data_list[5]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[5] = rate
            if rental_rates_min[5] == []:
                rental_rates_min[5] = '0'

    return rental_rates_min, is_vacant


if __name__ == '__main__':
    pass