# leduc_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
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


def bridgeport_manor():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = bridgeport_manor(); print('Rental rates:', d, c, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    bridgeport_min = dict()
    bridgeport_max = dict()
    is_vacant = []
    suite_types = ['3 Bed + Den']
    rental_rates_min = []
    rental_rates_max = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.greystonermc.ca/residential/bridgeport-manor'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the single rate for this property
    for i in page_parsed.findAll('span', 'suite-rate'):
        rate = i.text.strip()
        min_rate = rate[1:5]
        max_rate = rate[-4:]
        rental_rates_min.append(min_rate)
        rental_rates_max.append(max_rate)

    # grab vacancy status
    for j in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if str(j.text) == 'Available Now':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rate_max = rental_rates_max.pop(0)
        bridgeport_min[unit] = rate_min
        bridgeport_max[unit] = rate_max

    #print(bridgeport_min, bridgeport_max, is_vacant)
    return bridgeport_min, bridgeport_max, is_vacant


def bridgewood_apts():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = bridgewood_apts(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    bridgewood_min = dict()
    #bridgewood_max = dict()
    is_vacant = []
    suite_types = ['479 sqft', '668 sqft', '799 sqft', '825 sqft', '780 sqft']
    rental_rates_min = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.woodsmere.ca/property/bridgewood-apartments/'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental rates
    #for i in page_parsed.findAll('span', 'h2-big'):
    # rental_rates_min.append(i.text[1:-6])

    for j in page_parsed.findAll('div', 'col-md-1-4 col-xs-1-2'):
        temp = j.text.split()
        #print(temp)
        temp_first_item = temp[0]
        # append rental rate
        if temp_first_item[0] == '$':
            rent_rate = temp_first_item[1:-13]
            rental_rates_min.append(rent_rate)
            continue
        # append waitlist for suite
        if temp_first_item[0] == 'W':
            is_vacant.append('Waitlist')
            continue
        # append vacancy for suite
        if temp_first_item[0] == 'A':
            is_vacant.append(True)
            continue

    # print(rental_rates_min)
    # print(is_vacant)
    if rental_rates_min == []:
        return bridgewood_min, is_vacant

    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        bridgewood_min[unit] = rate

    #print(bridgewood_min, is_vacant)
    return bridgewood_min, is_vacant


def edgewood_estates():
    edgewood_suite_min = dict()
    suite_types = ['Meadow', 'Woodland', 'Briar']
    is_vacant = []
    url = 'https://alberta.weidner.com/apartments/ab/leduc/edgewood-estates/floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    script = park_scripts[63].text[292:-1500]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    script_list = script.split('}')
    #print(script_list)

    # meadow
    meadow = script_list[0]
    meadow = meadow[145:-205]
    meadow = meadow.split()
    #print(meadow)

    # woodland
    woodland = script_list[2]
    woodland = woodland[148:-205]
    woodland = woodland.split()
    #print(woodland)

    # briar
    briar = script_list[4]
    briar = briar[145:-130]
    briar = briar.split()
    #print(briar)

    rental_rates_min = [meadow[5], woodland[5], briar[5]]
    is_vacant = [meadow[7], woodland[7], briar[7]]

    # remove flaoting zeroes, commas, and dollar signs from string elements of rental_rates_min
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
        edgewood_suite_min[unit] = rent

    #print(edgewood_suite_min, is_vacant_final)
    return edgewood_suite_min, is_vacant_final


def leduc_mansion():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = leduc_mansion(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    mansion_min = dict()
    is_vacant = [False, False, False, False]
    suite_types = ['1 Bedroom', '2 Bedroom', '2 Bedroom 985 sqft', '3 Bedroom']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.bradenequitiesinc.com/property-listings/leduc-mansion-7128/'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    suite_index = {1: '1 bed 1 bath', 2: '2 bed 2 bath',
                   3: '2 bed 2 bath', 4: '3 bed 2 bath'}

    # grab suite cards
    suite_data = []
    for i in page_parsed.findAll('div', 'property-suite'):
        suite = i.text
        suite = suite.strip()
        current_suite_list = suite.split()
        suite_data.append(current_suite_list[:-2])

    # clean up the names of the suite titles, extract rental rates, adjust vacancy status, remove commas from rental rates
    suite_data = name_cleanup_leduc(suite_data)
    suite_data, is_vacant, rental_rates_min = find_rates_leduc(
        suite_data, is_vacant)
    rental_rates_min = remove_commas_leduc(rental_rates_min)

    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        if min_rate == []:
            mansion_min[unit] = '0'
        else:
            mansion_min[unit] = min_rate

    #print(mansion_min, is_vacant)
    return mansion_min, is_vacant


def remove_commas_leduc(rental_rates_min):
    """Removes commas from rental rates greater than $999"""
    for index, i in enumerate(rental_rates_min):
        if i != []:
            if i[1] == ',':
                rate = i
                rate = rate[0] + rate[2:]
                rental_rates_min[index] = rate
    return rental_rates_min


def find_rates_leduc(suite_data, is_vacant):
    """Extract the rental rates per suite card."""
    rental_rates_min = [[], [], [], []]
    for card in suite_data:
        # 1 bedroom
        if card[0] == '1':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[0] = rate
            is_vacant[0] = True

        # 2 bedroom
        """Monitor this over time because currently only 1 type of 2 bedroom is listed
        the excel sheet shows that there are 2 types of 2 bed suites but they do not post sq ft of each suite card (old info?)
        so there isn't currently anything to distinguish between the two types of suites since they only 
        post what is currently available"""
        if card[0] == '2':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[1] = rate
            is_vacant[1] = True

        # 2 bedroom (?) 985 sqft??
        if card[0] == '2':
            if rental_rates_min[1] != []:
                continue
            else:
                rate = card[-1]
                rate = rate[2:]
                rental_rates_min[2] = rate
                is_vacant[2] = True
        # 3 bedroom
        if card[0] == '3':
            rate = card[-1]
            rate = rate[2:]
            rental_rates_min[3] = rate
            is_vacant[3] = True

    return suite_data, is_vacant, rental_rates_min


def name_cleanup_leduc(suite_data):
    """Cleans up the suite type names ex: 'BedroomJun', 'BedroomFeb', etc."""
    for j in suite_data:
        # removes the month name at the end of the suite type name
        if j[0].isalpha() == True:
            if j[0] == 'Bachelor':
                pass
            else:
                j[0] = j[0][:-3]
        # removes the month name at the end of the suite type name
        if j[1].isalpha() == True:
            if j[1] == 'Bedroom':
                pass
            else:
                j[1] = j[1][:-3]
    return suite_data


def macewan_greens():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = macewan_greens(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    macewan_min = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.macewangreens.com/apartments-for-rent/leduc/1-bedroom/6201-grant-macewan-blvd/40875/plan/76679/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('p', 'col-sm-12 ypnh-propertypage-title-fp'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'break-two'):
        rental_rates_min.append(j.text[1:-6])

    '''VACANCY STATUS HAS NOT SHOW UP YET MAY 24 2022'''
    # find suite vacancy status
    for k in range(len(suite_types)):
        is_vacant.append('No Info')

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        macewan_min[unit] = rate

    #print(macewan_min, is_vacant)
    return macewan_min, is_vacant


def richmond_arms():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = richmond_arms(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    rich_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.har-par.com/properties.php?PropertyID=132'
    unico = 'http://www.har-par.com/properties.php?PropertyID=133'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('h4', 'media-heading'):
        suite_types.append(i.text)
    #print(suite_types)

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
        rich_min[unit] = rate_min

    #print(rich_min, is_vacant)
    return rich_min, is_vacant


def west_haven_terrace():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = west_haven_terrace(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    west_haven_min = dict()
    #west_haven_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.broadstreet.ca/residential/west-haven-terrace'
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
        west_haven_min[unit] = rate

    #print(west_haven_min, is_vacant)
    return west_haven_min, is_vacant


def unico_apts():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = unico_apts(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    unico_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.har-par.com/properties.php?PropertyID=133'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('h4', 'media-heading'):
        suite_types.append(i.text)
    #print(suite_types)

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
        unico_min[unit] = rate_min

    #print(unico_min, is_vacant)
    return unico_min, is_vacant


if __name__ == '__main__':
    pass

