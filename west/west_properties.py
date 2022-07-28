# west updater.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def tennyson_apts():
    tennyson_suite_min = dict()
    tennyson_suite_max = dict()
    suite_types = ['645 sqft', '892 sqft']
    is_vacant = [False, False]
    url = 'https://www.realstar.ca/apartments/ab/edmonton/tennyson-apartments/floorplans.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    """excel sheet on west sheet only accounts for 2 types of units, 
    645 sqft (1 br 1 bath) (variation A), 892 sqft (2br 2 bath) (variation C)"""
    # grab (#text <- .next_sibling of span sr-only class) for rents
    page_info = page_parsed.findAll('span', 'sr-only')
    span_class_text = []
    # reorganize the span 'sr-only' classes into a list
    for j in page_info:
        if j.next_sibling is None:
            continue
        ele = j.next_sibling.text.strip()
        span_class_text.append(ele)
    # extract rental rates per variation per suite type>(1 bed, 2 bed)
    suite_list, one_bed_data, two_bed_data = extract_rates(span_class_text)
    current_excel_list = [one_bed_data['1b A'], two_bed_data['2b C']]
    #print(current_excel_list)

    if len(current_excel_list[0]) != 2 and len(current_excel_list[0]) != 0:
        current_excel_list[0].append('0')
    if len(current_excel_list[1]) != 2 and len(current_excel_list[1]) != 0:
        current_excel_list[1].append('0')
    """just using var a and var c since excel sheet only looks for two rental rates currently
    ; to-do, account for all 6 suite_types/variations"""
    for unit in suite_types:
        rate_list = current_excel_list.pop(0)
        min_rate = rate_list[0]
        max_rate = rate_list[1]
        tennyson_suite_min[unit] = min_rate
        tennyson_suite_max[unit] = max_rate

    #print(tennyson_suite_min, tennyson_suite_max, is_vacant)
    return tennyson_suite_min, tennyson_suite_max, is_vacant


def str_clean(string):
    temp = string
    temp = temp.replace('$', '')
    temp = temp.replace('-', '')
    temp = temp.replace(',', '')
    temp = temp.strip()
    return temp


def extract_rates(span_class_text):
    """extract rental rates per type of suite + variation of suite type"""
    suite_list = [[], [], [], [], [], []]
    variation_data = {}
    variation = {'A': 1, 'B': 2, 'C': 3}
    rate_min_str = ''
    rate_max_str = ''
    # Variation A/B/C can exist in either 1 bed or 2 bed options
    bedroom_state = 1
    for index, i in enumerate(span_class_text):
        element = i

        # current<< flag for current variation currently on rotation in for loop
        if element[0:5] == 'Varia':
            current = element
            continue
        # 1 bed
        if element == '1 / 1':
            bedroom_state = 1
            continue
        # 2 bed
        if element == '2 / 2':
            bedroom_state = 2
            continue

        if element[0] == '$' and rate_min_str == '':
            rate_min_str = str_clean(element)

        # determines if min and max rate are offered; default max is 0 otherwise
        if element[-1] == '-':
            rate_min_str = str_clean(element)
            rate_max_str = str_clean(span_class_text[index+1])
            continue

        if rate_min_str != '':
            suite_index = variation[current[-1]]
            if bedroom_state == 1:
                suite_list[suite_index-1].append(rate_min_str)
                rate_min_str = ''
            if bedroom_state == 2:
                suite_list[suite_index+2].append(rate_min_str)
                rate_min_str = ''

        if rate_max_str != '':
            suite_index = variation[current[-1]]
            if bedroom_state == 1:
                suite_list[suite_index-1].append(rate_max_str)
                rate_max_str = ''
                continue
            if bedroom_state == 2:
                suite_list[suite_index+2].append(rate_max_str)
                rate_max_str = ''
                continue

    one_bed_data = {"1b A": suite_list[0], "1b B":
                    suite_list[1], "1b C": suite_list[2]}
    two_bed_data = {"2b A": suite_list[3], "2b B": suite_list[4], "2b C":
                    suite_list[5]}

    return suite_list, one_bed_data, two_bed_data

def cambrian_place():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = cambrian_place(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        cambrian_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        cambrian_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], [], [], [], []]
    suite_types = [[], [], [], [], [], []]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/cambrian-place/'
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

    card_list, is_vacant = get_vacancies_cambrian(
        temp_card_list, is_vacant, suite_types)
    cambrian_min, cambrian_max = get_rates(card_list, suite_types)
    #print(cambrian_min, cambrian_max); print(is_vacant)
    return cambrian_min, cambrian_max, is_vacant


def get_vacancies_cambrian(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], [], [], [], []]
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
                is_vacant[1] = card_list[1][3]
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

        # 3 bedroom
        if i[0] == '3' and i[2] != 'Premium':
            card_list[4] = i
            suite_types[4] = i[0] + f' {i[1]}'
            if card_list[4][2].isdigit():
                is_vacant[4] = card_list[4][2]
            if card_list[4][2] == 'Available':
                is_vacant[4] = True
            if card_list[4][2] == 'Waitlist':
                is_vacant[4] = False
            continue

        # 3 bedroom premium
        if i[0] == '3' and i[2] == 'Premium':
            card_list[5] = i
            suite_types[5] = i[0] + f' {i[1]} Premium'
            if card_list[5][3].isdigit():
                is_vacant[5] = card_list[5][3]
            if card_list[5][3] == 'Available':
                is_vacant[5] = True
            if card_list[5][3] == 'Waitlist':
                is_vacant[5] = False
            continue
    return card_list, is_vacant

def cambridge_west():
    cambridge_suite_min = dict()
    suite_types = ['Eton', 'Oxford', 'Windsor']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/cambridge-west/floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    # isolate script 64 and cut out large parts of the str(script), removing whitespace as well
    script = park_scripts[63].text[292:-1510]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()

    # since script is extremely long string, split it per '}' into list
    script_list = script.split('}')

    # Eton
    eton = script_list[0]
    eton = eton[140:-200]
    eton = eton.split()

    # Oxford
    oxford = script_list[2]
    oxford = oxford[148:-200]
    oxford = oxford.split()

    # Windsor
    windsor = script_list[4]
    windsor = windsor[153:]
    windsor = windsor.split()

    # order rental rates into list + vacancy numbers from 'availableCount:'
    rental_rates_min = [eton[5], oxford[5], windsor[5]]
    is_vacant = [eton[7], oxford[7], windsor[7]]

    # remove floating zeroes, commas and dollar signs from string elements
    rent_rates_final = []
    for i in rental_rates_min:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        rent_rates_final.append(i)

    # remove commas that can appear from 'availableCount' results
    is_vacant_final = []
    for j in is_vacant:
        j = j.replace(',', '')
        is_vacant_final.append(j)

    for unit in suite_types:
        rent = rent_rates_final.pop(0)
        cambridge_suite_min[unit] = rent

    #print(cambridge_suite_min, is_vacant_final)
    return cambridge_suite_min, is_vacant_final

def west_village():
    '''
    Excel sheet has 5 suite types but the website has 11?

    to follow with excel sheet i will scrape
    1 bed; 1 bed premium; 2 bed; 2 bed premium; 3 bed 

        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = west_village(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for west_village right now!
        west_village_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        west_village_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], [], [], []]
    suite_types = [[], [], [], [], []]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/west-edmonton-village/'
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

    card_list, is_vacant = get_vacancies_village(
        temp_card_list, is_vacant, suite_types)
    west_village_min, west_village_max = get_rates(card_list, suite_types)
    #print(west_village_min, west_village_max); print(is_vacant)
    return west_village_min, west_village_max, is_vacant


def morningside():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = morningside(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for morningside right now!
        morningside_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        morningside_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], [], []]
    suite_types = [[], [], [], []]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/morningside-estates/'
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

    card_list, is_vacant = get_vacancies_mornside(
        temp_card_list, is_vacant, suite_types)
    morningside_min, morningside_max = get_rates(card_list, suite_types)
    #print(morningside_min, morningside_max); print(is_vacant)
    return morningside_min, morningside_max, is_vacant


def webbergreens():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = webbergreens(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    webbergreens_min = dict()
    #webbergreens_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.broadstreet.ca/residential/webber-greens'
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
        webbergreens_min[unit] = rate

    #print(webbergreens_min, is_vacant)
    return webbergreens_min, is_vacant


def village_hamptons():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = village_hamptons(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    hamptons_min_rents = dict()
    suite_types = []
    is_vacant = []
    rent_rates_min = []
    url = 'https://premiumrentals.ca/properties/edmonton/village-at-the-hamptons/'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    """
    # possible solution to the connection being refused, yet to work though, might need a vpn? doesn't happen on my macbook air on the same network
    import time
    page = ''
    while page == '':
        try:
            page = requests.get(url, headers=headers)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("Trying again.")
            continue
    """
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the line of text that holds the suite type and rental starting rate for that suite
    for i in page_parsed.findAll('h4', 'uppercase text-left'):
        temp_list = i.text.strip().split()
        suite = str(temp_list[0] + ' ' + temp_list[1])
        suite_types.append(suite)
        # clean up the rental rate into an xxxx str format
        rent_rate = temp_list[4]
        rent_rate = rent_rate[1:]
        if rent_rate[1] == ',':
            rent_rate = rent_rate[0] + rent_rate[2:]
        rent_rates_min.append(rent_rate)

    # doesn't provide information on unit vacancy status, append 'No Info' == to length of suite_types
    for g in range(len(suite_types)):
        is_vacant.append('No Info')

    for unit in suite_types:
        rate = rent_rates_min.pop(0)
        hamptons_min_rents[unit] = rate

    #print(hamptons_min_rents, is_vacant)
    return hamptons_min_rents, is_vacant


def cedarville():
    '''
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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

    card_list, is_vacant = get_vacancies_cedar(
        temp_card_list, is_vacant, suite_types)
    cedarville_min, cedarville_max = get_rates(card_list, suite_types)
    #print(cedarville_min, cedarville_max); print(is_vacant)
    return cedarville_min, cedarville_max, is_vacant


def get_vacancies_cedar(temp_card_list, is_vacant, suite_types):
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


def get_vacancies_mornside(temp_card_list, is_vacant, suite_types):
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

def get_vacancies_village(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], [], [], []]
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

        if i[0] == '3':
            if i[2] != 'Premium' and i[2] != 'Townhouse' and i[2] != 'Bungalow':
                card_list[4] = i
                suite_types[4] = i[0] + f' {i[1]}'
                if card_list[4][2].isdigit():
                    is_vacant[4] = card_list[4][2]
                if card_list[4][2] == 'Available':
                    is_vacant[4] = True
                if card_list[4][2] == 'Waitlist':
                    is_vacant[4] = False
                continue
    return card_list, is_vacant


def get_rates(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    min_dict = dict()
    max_dict = dict()
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
        min_dict[unit] = min_rate
        max_dict[unit] = max_rate
    return min_dict, max_dict


if __name__ == '__main__':
    pass
