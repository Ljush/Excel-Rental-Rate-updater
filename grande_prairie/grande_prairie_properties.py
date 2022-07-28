# grande_prairie_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def carrington():
    carr_suite_min = dict()
    suite_types = ['Churchill', 'Aberdeen', 'Hudson', 'Pioneer']
    url = 'https://alberta.weidner.com/apartments/ab/grande-prairie/carrington-place/floorplans'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    # isolate script 64 and cut out large parts of the str(script)
    script = park_scripts[63].text[292:-1500]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    # since script is extremely long string, split it per '}' into list
    script_list = script.split('}')

    # churchill
    churchill = script_list[0]
    churchill = churchill[148:-212]
    churchill = churchill.split()
    #print(churchill)

    # aberdeen
    aberdeen = script_list[2]
    aberdeen = aberdeen[148:-205]
    aberdeen = aberdeen.split()
    #print(aberdeen)

    #hudson
    hudson = script_list[5]
    hudson = hudson[148:-205]
    hudson = hudson.split()
    #print(hudson)


    #pioneer
    pioneer = script_list[7]
    pioneer = pioneer[148:-12]
    pioneer = pioneer.split()
    #print(pioneer)

    rental_rates_min = [churchill[5], aberdeen[5], hudson[5], pioneer[5]]
    is_vacant = [churchill[7], aberdeen[7], hudson[7], pioneer[7]]

    min_rates_final = []
    for i in rental_rates_min:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        min_rates_final.append(i)

    # remove commas that can appear from 'availableCount' results
    is_vacant_final = []
    for j in is_vacant:
        j = j.replace(',', '')
        is_vacant_final.append(j)

    #build dictionary of rental rates per suite type
    for unit in suite_types:
        rent = min_rates_final.pop(0)
        carr_suite_min[unit] = rent

    #print(carr_suite_min, is_vacant_final)
    return carr_suite_min, is_vacant_final


def gateway():
    gate_suite_min = dict()
    is_vacant = [False, False, False, False, False]
    rental_rates_min = [[], [], [], [], []]
    suite_types = ['1 Bedroom', '2 Bedroom 668 sqft', '2 Bedroom 780 sqft',
                   '2 Bedroom 799 sqft', '2 Bedroom 825 sqft']
    url = 'https://www.woodsmere.ca/property/gateway-apartments/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # extract suite card information
    suite_cards = page_parsed.findAll('div', 'frow botbor items-center')
    info_suite_card = []
    for i in suite_cards:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.strip()
        element = element.split()
        info_suite_card.append(element)
    """there is nothing to determine which element of suite_cards list 
    is what type of suite so for now we will assume that the order 
    that gateway posts their suites does not change in accordance 
    to the excel sheet"""

    # extract rental rate and vacancy status
    for j in info_suite_card:
        # 1 bedroom
        if '479floorplan' in j:
            if j[-2] == 'Wait':
                is_vacant[0] = False
            if j[-2] == 'Apply':
                is_vacant[0] = True
            rate = j[0]
            rate = rate[:-6]
            rate = rate.replace('$', '')
            rate = rate.replace('/month', '')
            rental_rates_min[0] = rate
            continue

        # 2 bedroom - 668 sqft
        if '668floorplan' in j:
            if j[-2] == 'Wait':
                is_vacant[1] = False
            if j[-2] == 'Apply':
                is_vacant[1] = True
            rate = j[0]
            rate = rate[:-6]
            rate = rate.replace('$', '')
            rate = rate.replace('/month', '')
            rental_rates_min[1] = rate
            continue

        # 2 bedroom - 780 sqft
        if '780floorplan' in j:
            if j[-2] == 'Wait':
                is_vacant[2] = False
            if j[-2] == 'Apply':
                is_vacant[2] = True
            rate = j[0]
            rate = rate[:-6]
            rate = rate.replace('$', '')
            rate = rate.replace('/month', '')
            rental_rates_min[2] = rate
            continue

        # 2 bedroom - 799 sqft
        if '799floorplan' in j:
            if j[-2] == 'Wait':
                is_vacant[3] = False
            if j[-2] == 'Apply':
                is_vacant[3] = True
            rate = j[0]
            rate = rate[:-6]
            rate = rate.replace('$', '')
            rate = rate.replace('/month', '')
            rental_rates_min[3] = rate
            continue

        # 2 bedroom - 825 sqft
        if '825floorplan' in j:
            if j[-2] == 'Wait':
                is_vacant[4] = False
            if j[-2] == 'Apply':
                is_vacant[4] = True
            rate = j[0]
            rate = rate[:-6]
            rate = rate.replace('$', '')
            rate = rate.replace('/month', '')
            rental_rates_min[4] = rate
            continue

    # build dictionary for min rates per suite type
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        gate_suite_min[unit] = min_rate

    #print(gate_suite_min); print(is_vacant)
    return gate_suite_min, is_vacant


def lexington():
    lex_suite_min = dict()
    is_vacant = [[], [], []]
    rental_rates_min = [[], [], []]
    suite_types = ['Sheridan', 'Renaissance', 'Legacy']
    url = 'https://www.nalgp.com/properties/9-the-lexington'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # extract suite card information
    suite_cards = page_parsed.findAll('div', 'djc_item_in djc_clearfix')
    info_suite_card = []
    for i in suite_cards:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.strip()
        element = element.split()
        element = element[:-1]
        info_suite_card.append(element)

    # extract vacancy status and rental rate of suite type
    for j in info_suite_card:
        # sheridan
        if 'Sheridan' in j:
            # get rent rate
            for current in j:
                if current[0].isdigit() == True:
                    # ex: 1050.00 (rate) -> 200.00 (deposit for suite) (dont want the deposits)
                    if len(current) > 6:
                        rate = current[:-3]
                        rental_rates_min[0] = rate
            # check vacancy status
            if j[-2] == 'Not':
                is_vacant[0] = False
            if j[-2] == 'Apply':
                is_vacant[0] = True

        # renaissance
        if 'Renaissance' in j:
            # get rent rate
            for current in j:
                if current[0].isdigit() == True:
                    # ex: 1050.00 (rate) -> 200.00 (deposit for suite) (dont want the deposits)
                    if len(current) > 6:
                        rate = current[:-3]
                        rental_rates_min[1] = rate
            # check vacancy status
            if j[-2] == 'Not':
                is_vacant[1] = False
            if j[-2] == 'Apply':
                is_vacant[1] = True

        # Legacy
        if 'Legacy' in j:
            # get rent rate
            for current in j:
                if current[0].isdigit() == True:
                    # ex: 1050.00 (rate) -> 200.00 (deposit for suite) (dont want the deposits)
                    if len(current) > 6:
                        rate = current[:-3]
                        rental_rates_min[2] = rate
            # check vacancy status
            if j[-2] == 'Not':
                is_vacant[2] = False
            if j[-2] == 'Apply':
                is_vacant[2] = True

    # build dictionary for min rates per suite type
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        lex_suite_min[unit] = min_rate

    #print(lex_suite_min); print(is_vacant)
    return lex_suite_min, is_vacant


def northgate():
    north_suite_min = dict()
    is_vacant = [False, False]
    rental_rates_min = [[], []]
    suite_types = ['1 Bedroom', '2 Bedroom']
    url = 'https://www.rentnorthview.com/apartments/northgate-iii-northgate-apartments'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # extract suite card information
    suite_cards = page_parsed.findAll('tr', 'no-description')
    info_suite_card = []
    for i in suite_cards:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.strip()
        element = element.split()
        info_suite_card.append(element)

    # extract rental rates and vacancy status per suite card
    for j in info_suite_card:
        # 1 bedroom + den
        if j[2] == '1':
            # check status of vacant units
            if 'Not' or 'Sorry' in j:
                is_vacant[0] = False
            if 'Check' in j:
                is_vacant[0] = True
            # iterate thru list to find rental rate
            for current in j:
                if current[0] == '$':
                    rate = current.replace('$', '')
                    rental_rates_min[0] = rate
                    continue

        # 2 bedroom
        if j[2] == '2':
            # check status of vacant units
            if 'Not' or 'Sorry' in j:
                is_vacant[1] = False
            if 'Check' in j:
                is_vacant[1] = True
            # iterate thru list to find rental rate
            for current in j:
                if current[0] == '$':
                    rate = current.replace('$', '')
                    rental_rates_min[1] = rate
                    continue

    # build dictionary of min rates per suite types
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        north_suite_min[unit] = min_rate

    #print(north_suite_min); print(is_vacant)
    return north_suite_min, is_vacant


def westmore():
    west_suite_min = dict()
    is_vacant = [False, False]
    rental_rates_min = [[], []]
    suite_types = ['1 Bedroom', '2 Bedroom']
    url = 'https://www.rentnorthview.com/apartments/westmore-estates'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # extract suite card information
    suite_cards = page_parsed.findAll('tr', 'no-description')
    info_suite_card = []
    for i in suite_cards:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.strip()
        element = element.split()
        info_suite_card.append(element)

    # extract rental rates and vacancy status per suite card
    for j in info_suite_card:
        # 1 bedroom + den
        if j[2] == '1':
            # check status of vacant units
            if 'Not' or 'Sorry' in j:
                is_vacant[0] = False
            if 'Check' in j:
                is_vacant[0] = True
            # iterate thru list to find rental rate
            for current in j:
                if current[0] == '$':
                    rate = current.replace('$', '')
                    rental_rates_min[0] = rate
                    continue

        # 2 bedroom
        if j[2] == '2':
            # check status of vacant units
            if 'Not' or 'Sorry' in j:
                is_vacant[1] = False
            if 'Check' in j:
                is_vacant[1] = True
            # iterate thru list to find rental rate
            for current in j:
                if current[0] == '$':
                    rate = current.replace('$', '')
                    rental_rates_min[1] = rate
                    continue

    # build dictionary of min rates per suite types
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        west_suite_min[unit] = min_rate

    #print(west_suite_min); print(is_vacant)
    return west_suite_min, is_vacant


def willowbrook():
    willow_suite_min = dict()
    willow_suite_max = dict()
    suite_types = ['Riesling', 'Cabernet', 'Malbec', 'Merlot', 'Shiraz']
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info', 'No Info']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://highstreetliving.ca/locations/grande-prairie-willowbrook/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the individual suite card data
    suite_cards = page_parsed.findAll('div', 'wpb_wrapper')
    suite_card_list = []
    for i in suite_cards:
        temp = i.text
        temp = temp.replace('\n', ' ')
        temp = temp.replace('\t', ' ')
        temp = temp.strip()
        temp_list = temp.split()

        # some lists were empty, or way too long and not what we are looking for
        if len(temp_list) <= 100 and len(temp_list) > 12:
            if temp_list[0] in suite_types:
                suite_card_list.append(temp_list)

    # extract rental rates min/max
    count = 0
    for j in suite_card_list:
        for k in j:
            # finds specific rate, remove $ and * elements from string
            if k[0] == '$':
                rate = k
                rate = rate.replace('$', '')
                rate = rate.replace('*', '')
                # checking if count is even/odd distinguishes whether rate is
                # a minimum rate or maximum rate
                if count % 2 == 0:
                    rental_rates_min.append(rate)
                    count += 1
                else:
                    rental_rates_max.append(rate)
                    count += 1

    # build min/max dictionaries with rents to suite types
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        willow_suite_min[unit] = min_rate
        willow_suite_max[unit] = max_rate

    #print(willow_suite_min); print(willow_suite_max); print(is_vacant)
    return willow_suite_min, willow_suite_max, is_vacant

def northland():
    land_suite_min = dict()
    is_vacant = [[], [], [], []]
    rental_rates_min = [[], [], [], []]
    suite_types = ['Bachelor', '1 Bedroom', '2 Bedroom', '2 Bedroom 2 Bath']
    url = 'https://www.northlandmanagement.ca/residential-properties/grande-prairie/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite card information
    suite_cards = page_parsed.findAll('div', 'suite suite-block')
    suite_card_info = []
    for i in suite_cards:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', '')
        element = element.strip()
        element = element.split()
        element = element[2:]
        suite_card_info.append(element)

    # template of suite_card_info (june 16, 2022)
    """['1', 'Bed,', '1', 'Bath', '620sq.', 'ft.', '$900/month', 'Yes']
    ['2', 'Bed,', '1', 'Bath', '740', '-', '754sq.', 'ft.', '$1000/month', 'Yes']
    ['2', 'Bed,', '2', 'Bath', '870sq.', 'ft.', '$1100/month', 'No']
    ['Bachelor', '424sq.', 'ft.', '$850/month', 'Yes']"""

    # extract rental rates
    for j in suite_card_info:
        # bachelor
        if j[0] == 'Bachelor':
            # get rate
            bachelor_rate = j[-2]
            bachelor_rate = bachelor_rate.replace('$', '')
            bachelor_rate = bachelor_rate.replace('/month', '')
            rental_rates_min[0] = bachelor_rate
            # check vacancy status
            if j[-1] == 'Yes':
                is_vacant[0] = True
            if j[-1] == 'No':
                is_vacant[0] = False
            continue

        # 1 bedroom
        if j[0] == '1':
            # get rate
            one_rate = j[-2]
            one_rate = one_rate.replace('$', '')
            one_rate = one_rate.replace('/month', '')
            rental_rates_min[1] = one_rate
            # check vacancy status
            if j[-1] == 'Yes':
                is_vacant[1] = True
            if j[-1] == 'No':
                is_vacant[1] = False
            continue

        # 2 bedroom
        if j[0] == '2' and j[2] != '2':
            # get rate
            two_rate = j[-2]
            two_rate = two_rate.replace('$', '')
            two_rate = two_rate.replace('/month', '')
            rental_rates_min[2] = two_rate
            # check vacancy status
            if j[-1] == 'Yes':
                is_vacant[2] = True
            if j[-1] == 'No':
                is_vacant[2] = False
            continue

        # 2 bedroom 2 bath
        if j[0] == '2' and j[2] == '2':
            # get rate
            last_rate = j[-2]
            last_rate = last_rate.replace('$', '')
            last_rate = last_rate.replace('/month', '')
            rental_rates_min[3] = last_rate
            # check vacancy status
            if j[-1] == 'Yes':
                is_vacant[3] = True
            if j[-1] == 'No':
                is_vacant[3] = False
            continue

    # build dictionary for min rate per suite type
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        land_suite_min[unit] = min_rate

    #print(land_suite_min); print(is_vacant)
    return land_suite_min, is_vacant


def prairie_sunrise():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = prairie_sunrise(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        sunrise_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        sunrise_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.'''
    is_vacant = [[], [], [], []]
    suite_types = [[], [], [], []]
    url = 'https://www.bwalk.com/en-ca/rent/details/alberta/grande-prairie/prairie-sunrise-towers/'
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

    card_list, is_vacant = get_vacancies_prairie(
        temp_card_list, is_vacant, suite_types)
    sunrise_min, sunrise_max = get_rates_prairie(card_list, suite_types)
    #print(sunrise_min); print(sunrise_max); print(is_vacant)
    return sunrise_min, sunrise_max, is_vacant


def get_vacancies_prairie(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], [], []]
    for i in temp_card_list:
        #print(i)
        # bachelor
        if i[0] == 'Bachelor':
            card_list[0] = i
            suite_types[0] = 'Bachelor'
            if card_list[0][1].isdigit():
                is_vacant[0] = card_list[0][1]
            if card_list[0][1] == 'Available':
                is_vacant[0] = True
            if card_list[0][1] == 'Waitlist':
                is_vacant[0] = False
            continue

        # 1 bedroom
        if i[0] == '1':
            card_list[1] = i
            suite_types[1] = '1 Bedroom'
            if card_list[1][2].isdigit():
                is_vacant[1] = card_list[1][2]
            if card_list[1][2] == 'Available':
                is_vacant[1] = True
            if card_list[1][2] == 'Waitlist':
                is_vacant[1] = False
            continue

        # 2 bedroom
        if i[0] == '2' and i[2] != 'Premium' and i[2] != 'Penthouse':
            card_list[2] = i
            suite_types[2] = '2 Bedroom'
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
            suite_types[3] = '2 Bedroom Premium'
            if card_list[3][3].isdigit():
                is_vacant[3] = card_list[3][3]
            if card_list[3][3] == 'Available':
                is_vacant[3] = True
            if card_list[3][3] == 'Waitlist':
                is_vacant[3] = False
            continue
    return card_list, is_vacant


def get_rates_prairie(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    sunrise_min = dict()
    sunrise_max = dict()
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
        sunrise_min[unit] = min_rate
        sunrise_max[unit] = max_rate
    return sunrise_min, sunrise_max


if __name__ == '__main__':
    pass