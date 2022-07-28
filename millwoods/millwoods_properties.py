# millwoods_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def amblewood_terrace():
    """
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = amblewood_terrace(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
            vacancy bools (is_vacant)
        
    Vars:
    amble_suites_min (dict) - Minimum rates + unit types 
    amble_suites_max (dict) - Maximum rates + unit types 
    is_vacant (list)        - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            amble_suites_min, amble_suites_max, is_vacant"""

    amble_suites_min = dict()
    amble_suites_max = dict()
    suite_types = []
    min_rates = []
    max_rates = []
    is_vacant = []
    url = 'https://www.parabelle.com/apartments/8103-29-ave-amblewood-ter/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('span', 'suite-type'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'suite-rate'):
        temp = j.text.strip().split()
        min_ = temp[0]
        min_ = min_[1:]

        max_ = temp[-1]
        max_ = max_[1:]

        if max_[1] == ',':
            max_ = max_[0:1] + max_[2:]
        if min_[1] == ',':
            min_ = min_[0:1] + min_[2:]
        min_rates.append(min_)
        max_rates.append(max_)

    # find suite vacancy status
    for x in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if x.text == 'Notify me':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        _min = min_rates.pop(0)
        _max = max_rates.pop(0)
        amble_suites_min[unit] = _min
        amble_suites_max[unit] = _max

    #print(amble_suites_min, amble_suites_max, is_vacant)
    return amble_suites_min, amble_suites_max, is_vacant


def ascot_court():
    """ 
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = ascot_court(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
            vacancy bools (is_vacant)
    Vars:
    ascot_suites_min (dict) - Minimum rates + unit types 
    ascot_suites_max (dict) - Maximum rates + unit types 
    is_vacant (list)        - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            ascot_suites_min, ascot_suites_max, is_vacant"""

    ascot_suites_min = dict()
    ascot_suites_max = dict()
    suite_types = []
    min_rates = []
    max_rates = []
    is_vacant = []
    url = 'https://www.parabelle.com/apartments/4055-26-ave-ascot-ct/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('span', 'suite-type'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'suite-rate'):
        temp = j.text.strip().split()
        min_ = temp[0]
        min_ = min_[1:]
        max_ = temp[-1]
        max_ = max_[1:]

        if max_[1] == ',':
            max_ = max_[0:1] + max_[2:]
        if min_[1] == ',':
            min_ = min_[0:1] + min_[2:]
        min_rates.append(min_)
        max_rates.append(max_)

    # find suite vacancy status
    for x in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if x.text == 'Notify me':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        _min = min_rates.pop(0)
        _max = max_rates.pop(0)
        ascot_suites_min[unit] = _min
        ascot_suites_max[unit] = _max

    #print(ascot_suites_min, ascot_suites_max, is_vacant)
    return ascot_suites_min, ascot_suites_max, is_vacant


def avalon_court():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = avalon_court(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    avalon_min = dict()
    avalon_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    rental_rates_max = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.avenueliving.ca/apartments-for-rent/avalon-court'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('div', 'suite-type cell'):
        suite_types.append(i.text.strip()[8:])

    # grab rental rates per suite type
    for j in page_parsed.findAll('div', 'suite-rate cell'):
        temp_ = j.text.strip()
        temp_ = temp_[1:]
        temp_list = temp_.split('-')
        if len(temp_list) > 1:
            max_rate = temp_list[1]
            max_rate = max_rate[1:]
            rental_rates_min.append(temp_list[0])
            rental_rates_max.append(max_rate)
        else:
            rental_rates_min.append(temp_list[0])
            rental_rates_max.append(temp_list[0])

    for x in page_parsed.findAll('div', 'suite-availability cell'):
        temp = x.text.strip()
        temp = temp.replace('\n', '')
        if temp == 'Book a Showing':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rate_max = rental_rates_max.pop(0)
        avalon_min[unit] = rate_min
        avalon_max[unit] = rate_max

    #print(avalon_min, avalon_max, is_vacant)
    return avalon_min, avalon_max, is_vacant


def hillview_park():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = hillview_park(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    hillview_min = dict()
    is_vacant = [False, False]
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = ['0', '0']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.aimrealestate.ca/b/20173529310000422506'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rent range
    rent_data_list = []
    for j in page_parsed.findAll('a', 'apartment-view-potential'):
        element = j.text
        element = element.replace('\n', ' ')
        element = element.strip()
        element = element.split()
        rent_data_list.append(element)

    for x in rent_data_list:
        """ Template of resulting suite card row from website
        ['207', '$1,050', '--', '2', '1', 'Available', 'Now!']"""
        # 2 bedroom
        if x[3] == '2':
            rate = x[1]
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            rental_rates_min[1] = rate
            is_vacant[1] = True

        # 1 bedroom
        if x[3] == '1':
            rate = x[1]
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            rental_rates_min[0] = rate
            is_vacant[0] = True

    # build min rate dictionary from rental_rates_min
    for unit in suite_types:
        temp = rental_rates_min.pop(0)
        hillview_min[unit] = temp

    #print(hillview_min, is_vacant)
    return hillview_min, is_vacant


def laurel_gardens():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = laurel_gardens(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    laurel_min = dict()
    #laurel_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.broadstreet.ca/residential/laurel-gardens'
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
        laurel_min[unit] = rate

    #print(laurel_min, is_vacant)
    return laurel_min, is_vacant


def laurel_meadows():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = laurel_meadows(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
            vacancy bools (is_vacant)'''
    laurel_min = dict()
    #laurel_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.broadstreet.ca/residential/laurel-meadows'
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
        laurel_min[unit] = rate

    #print(laurel_min, is_vacant)
    return laurel_min, is_vacant


def leewood_village():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = leewood_village(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        leewood_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        leewood_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], []]
    suite_types = [[], [], []]
    page = requests.get('https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/leewood-village/')
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

    card_list, is_vacant = get_vacancies_leewood(temp_card_list, is_vacant, suite_types)
    leewood_suite_min, leewood_suite_max = get_rates_leewood(
        card_list, suite_types)
    #print(leewood_suite_min, leewood_suite_max); print(is_vacant)
    return leewood_suite_min, leewood_suite_max, is_vacant


def millcrest_apts():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = southwood_arms(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
            vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        mill_suites_min (dict)     - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    mill_suites_min = dict()
    #mill_suites_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/millcrest-apts'
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

    # iterate thru suite_types and rental_rates to create the mill_suites_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        mill_suites_min[unit] = temp

    #print(mill_suites_min, is_vacant)
    return mill_suites_min, is_vacant


def ridgewood_court():
    """
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = ridgewood_court(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
    ridgewood_suites_min (dict) - Minimum rates + unit types 
    ridgewood_suites_max (dict) - Maximum rates + unit types 
    is_vacant (list)           - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            ridgewood_suites_min, ridgewood_suites_max, is_vacant"""

    ridgewood_suites_min = dict()
    ridgewood_suites_max = dict()
    suite_types = []
    min_rates = []
    max_rates = []
    is_vacant = []
    url = 'https://www.parabelle.com/apartments/2303-38-st-ridgewood-ct'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('span', 'suite-type'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'suite-rate'):
        temp = j.text.strip().split()
        min_ = temp[0]
        max_ = temp[-1]
        min_ = min_[1:]
        max_ = max_[1:]

        if max_[1] == ',':
            max_ = max_[0:1] + max_[2:]
        if min_[1] == ',':
            min_ = min_[0:1] + min_[2:]
        min_rates.append(min_)
        max_rates.append(max_)

    # find suite vacancy status
    for x in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if x.text == 'Notify me':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        _min = min_rates.pop(0)
        _max = max_rates.pop(0)
        ridgewood_suites_min[unit] = _min
        ridgewood_suites_max[unit] = _max

    #print(ridgewood_suites_min, ridgewood_suites_max, is_vacant)
    return ridgewood_suites_min, ridgewood_suites_max, is_vacant


def ridgewood_manor():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = ridgewood_manor(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    rid_manor_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.har-par.com/properties.php?PropertyID=55'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('h4', 'media-heading'):
        suite_types.append(i.text)

    # grab rental rates per suite type
    for j in page_parsed.findAll('li'):
        if j.text[:4] == 'Rent' and j.text[-1].isdigit():
            rent_rate = j.text[-4:]
            if rent_rate[0] == '$':
                rent_rate = rent_rate[1:]
                rental_rates_min.append(rent_rate)
            else:
                rental_rates_min.append(rent_rate)

    for x in page_parsed.findAll('div', 'col-xs-3 stat text-center'):
        temp = x.text.split()
        if temp[0] == 'No':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rid_manor_min[unit] = rate_min

    #print(rid_manor_min, is_vacant)
    return rid_manor_min, is_vacant


def ridgewood_park():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = ridgewood_park(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    rid_park_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.har-par.com/properties.php?PropertyID=56'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('h4', 'media-heading'):
        suite_types.append(i.text)

    # grab rental rates per suite type
    for j in page_parsed.findAll('li'):
        if j.text[:4] == 'Rent' and j.text[-1].isdigit():
            rent_rate = j.text[-4:]
            if rent_rate[0] == '$':
                rent_rate = rent_rate[1:]
                rental_rates_min.append(rent_rate)
            else:
                rental_rates_min.append(rent_rate)

    for x in page_parsed.findAll('div', 'col-xs-3 stat text-center'):
        temp = x.text.split()
        if temp[0] == 'No':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rid_park_min[unit] = rate_min

    #print(rid_park_min, is_vacant)
    return rid_park_min, is_vacant


def sandstone_pointe():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = sandstone_pointe(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        sand_suites_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        sand_suites_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans or ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], []]
    suite_types = [[], [], []]
    page = requests.get(
        'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/sandstone-pointe/')
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

    card_list, is_vacant = get_vacancies_sandstone(
        temp_card_list, is_vacant, suite_types)
    sand_suites_min, sand_suites_max = get_rates_sandstone(
        card_list, suite_types)
    #print(sand_suites_min, sand_suites_max); print(is_vacant)
    return sand_suites_min, sand_suites_max, is_vacant


def get_vacancies_sandstone(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], []]
    for i in temp_card_list:
        # 1 bedroom
        if i[0] == '1' and i[2] != 'Premium':
            card_list[0] = i
            suite_types[0] = i[0] + f' {i[1]}'
            if card_list[0][2].isdigit():
                is_vacant[0] = card_list[0][2]
            if card_list[0][2] == 'Available':
                is_vacant[0] = True
            if card_list[0][2] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 2 bedroom + den
        if i[0] == '2' and i[2] == '+':
            card_list[2] = i
            suite_types[2] = i[0] + f' {i[1]} + Den'
            if card_list[2][4].isdigit():
                is_vacant[2] = card_list[2][4]
            if card_list[2][4] == 'Available':
                is_vacant[2] = True
            if card_list[2][4] == 'Waitlist':
                is_vacant[2] = False
            continue

        # 2 bedroom
        if i[0] == '2' and i[2] != 'Premium':
            if i[2] != 'Bi-Level' and i[2] != 'Bi-level':
                card_list[1] = i
                suite_types[1] = i[0] + f' {i[1]}'
                if card_list[1][2].isdigit():
                    is_vacant[1] = card_list[1][2]
                if card_list[1][2] == 'Available':
                    is_vacant[1] = True
                if card_list[1][2] == 'Waitlist':
                    is_vacant[1] = False
                continue
    return card_list, is_vacant


def get_rates_sandstone(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    sand_suites_min = dict()
    sand_suites_max = dict()
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
        sand_suites_min[unit] = min_rate
        sand_suites_max[unit] = max_rate
    return sand_suites_min, sand_suites_max

def get_vacancies_leewood(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], []]
    for i in temp_card_list:
        # 1 bedroom
        if i[0] == '1' and i[2] != 'Premium':
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
        if i[0] == '2' and i[2] != 'Premium':
            card_list[1] = i
            suite_types[1] = i[0] + f' {i[1]}'
            if card_list[1][2].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][2] == 'Available':
                is_vacant[1] = True
            if card_list[1][2] == 'Waitlist':
                is_vacant[1] = False
            continue
    return card_list, is_vacant

def get_rates_leewood(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    leewood_suite_min = dict()
    leewood_suite_max = dict()
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
        leewood_suite_min[unit] = min_rate
        leewood_suite_max[unit] = max_rate
    return leewood_suite_min, leewood_suite_max

if __name__ == '__main__':
    pass