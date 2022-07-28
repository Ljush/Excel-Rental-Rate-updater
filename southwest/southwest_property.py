# southwest_property.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def ashbrook():
    """Considering this a rough draft until all other properties for the other
    sheets in Alberta are created, and followed through testing of a few months
    throughout the year.
    
    Since these scripts involve webscraping to gather such a small but albeit
    specific range of information, I expect these to eventually be 
    rewritten to be more readily and easily maintained by someone other 
    than myself simply because I believe that some of the competitors will 
    sell the property to a different company and/or change the general 
    structure of their property website in general.
    
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = ashbrook(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
    ash_suite_types_min (dict) - Minimum rates + unit types 
    ash_suite_types_max (dict) - Maximum rates + unit types 
    is_vacant (list)           - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the ashbrook webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            ash_suite_types_min, ash_suite_types_max, is_vacant"""
    ash_suite_types_min = dict()
    ash_suite_types_max = dict()
    is_vacant = []

    page = requests.get(
        'https://www.parabelle.com/apartments/3955-114-st-ashbrook')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    find_vacancies_tab = page_parsed.find('div', 'suite-info-container')
    vacancy_box_data = find_vacancies_tab.findAll('a')

    for s in vacancy_box_data:
        #print('entry:', s.text, type(s))
        if 'Available Now' in s:
            vacant = True
            is_vacant.append(vacant)
            continue
       # if 'Notify me' in s:
        else:
            vacant = False
            is_vacant.append(vacant)
            continue

    suite = page_parsed.find('div', 'suites-boxes')
    rents = suite.findAll('span')

    for i in rents:
        if i.text == '1 Bedroom':
            suite_type = i.text
            continue
        if i.text == '1 Bedroom + Den':
            suite_type = i.text
            continue
        if i.text == '2 Bedrooms':  # and i.text[-1] == 's':
            suite_type = i.text
            continue
        if i.text == '2 Bedroom + Den':  # and i.text[-1] == 'n':
            suite_type = i.text
            continue
        if i.text[5] == '$':
            minimum = i.text[6:11]
            ash_suite_types_min[suite_type] = minimum
            try:
                maximum = i.text[15:20]
                if maximum[0] == ' ':
                    ash_suite_types_max[suite_type] = ''
                    continue
                ash_suite_types_max[suite_type] = maximum
            except:
                #print('No maximum rate for this unit')
                ash_suite_types_max[suite_type] = ''
                continue
    #print('MIN RATES:', ash_suite_types_min, '\n','MAX RATES:', ash_suite_types_max)
    #print('VACANCIES:', is_vacant)
    return ash_suite_types_min, ash_suite_types_max, is_vacant


def wellington_court():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    wellington_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    sq_ft_variations = []
    url = 'https://www.realstar.ca/apartments/ab/edmonton/wellington-court-apartments/floorplans.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab variation titles
    wellington_data = page_parsed.findAll('div', 'accordion-inner')
    # for i in wellington_data:
    #     element = i.text
    #     element = element.replace('\n', ' ')
    #     element = element.replace('\t', ' ')
    #     element = element.strip()
    #     element = element.split()
    #     print(repr(element))
    pass

def blue_quill():
    '''Exactly the same logic as pineridge_grabber.py
    
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = blue_quill(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    blue_quill_rents = dict()
    blue_suite_types = []
    is_vacant = []
    suite_info = []
    url = 'http://www.har-par.com/properties.php?PropertyID=6'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    blue_quill = requests.get(url, headers=headers)
    blue_soup = BeautifulSoup(blue_quill.content, 'html.parser')
    blue_description = blue_soup.select('body div.row.property-unit')

    for suite in blue_description:
        suite_info.append(suite.text.replace('\n', ' ').split())

    count = 0
    for data in suite_info:
        if data[-1] == 'Vacancy':
            is_vacant.append(False)

        if data[-1] == 'Apply':
            is_vacant.append(True)

        for info in data:
            # removes odd $xxxrent elements from a list
            if info[0] == '$' and info[-1] == 't':
                data.remove(info)
                continue

            if info[0] == '$' and int(info[1:]) < 849:
                data.remove(info)
                continue

            if data[0].isnumeric():
                if data[1].isalpha():
                    new_type = str(data[0]) + f' {data[1]}'
                    blue_suite_types.append(new_type)
                    data.remove(info)

            if info[0] == '$':
                blue_quill_rents[blue_suite_types[count]] = info[1:]
                data.remove(info)
                count += 1

    #print(blue_quill_rents, is_vacant)
    return blue_quill_rents, is_vacant


def cornerstone_callaghan():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE
    1 - right click -> Run Current File in Interactive Window
    2 - paste -> >  d, x = cornerstone_callaghan()
    print('Rental rates:', d, '\nVacancies:', x)
    3 - run the code to visualize what the dictionary of units and list of
    vacancy bools(is_vacant)
    
    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    cornerstone_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    page = requests.get(
        'https://www.broadstreet.ca/residential/cornerstone-at-callaghan')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite names
    for i in page_parsed.findAll('span', 'suite__name--text'):
        suite_types.append(i.text)
    #print(suite_types)

    # grab rental rates per suite
    for j in page_parsed.findAll('span', 'suite__rate--text'):
        rental_rates_min.append(j.text[1:])
    #print(rental_rates_min)

    # grab availability of suites (vacancies)
    for k in page_parsed.findAll('span', 'suite__availability-text--text'):
        is_vacant.append(k.text[0])
    #print(is_vacant)

    for unit in suite_types:
        temp = rental_rates_min.pop(0)
        cornerstone_suite_min[unit] = temp

    #print(cornerstone_suite_min, is_vacant)
    return cornerstone_suite_min, is_vacant


def southwood_arms():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = southwood_arms(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        southwood_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    southwood_suite_min = dict()
    #southwood_suite_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/southwood-arms'
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

    # iterate thru suite_types and rental_rates to create the southwood_suite_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        southwood_suite_min[unit] = temp

    #print(southwood_suite_min, is_vacant)
    return southwood_suite_min, is_vacant


def the_village():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = the_village(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        village_suite_min (dict)    - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)            - list of booleans whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        reordered_suites (list)     - reorder the list of suite types to better
                                      fit with the 
        reordered_min_rates (list)  - for min rents; see reordered_suites (list)'''
    village_suite_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    # midwest has updated cloudflare to flag botting? we use navigation.useragent
    # data from the midwest village website to bypass the '403 forbidden' error to bypass this lol
    url = 'https://rentmidwest.com/location/the-village-at-southgate-edmonton-apartment-rental/'
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

    for j in details_2:
        rate_temp = j.text.replace('\n', '')
        rate = rate_temp[12:-3]
        rental_rates_min.append(rate)

    for unit in suite_types:
        rent_rate = rental_rates_min.pop(0)
        village_suite_min[unit] = rent_rate

    for vacancy in range(len(suite_types)):
        is_vacant.append('Waitlist')

    #print(village_suite_min, '\n', is_vacant)
    return village_suite_min, is_vacant

def rideau_place():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = rideau_place(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)

    Vars:
        No max rates for rideau place right now!
        rideau_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)        - list of booleans whether the unit has vacancy or not
        suite_types (list)      - 1 bed, 2 bed, 3 bed etc. as of may 10/2022 
                                  3 beds are not listed on the site but i think 
                                  this script would manage its appearance just fine.
        suite_rental_rates(list)- '$xxx' rental rates per suite'''
    rideau_suite_min = dict()
    #rideau_suite_max = dict()
    is_vacant = []
    suite_types = []
    suite_rental_rates = []
    # grab the rideau place URL and parse it with beautifulsoup
    page = requests.get(
        'https://www.mmgltd.com/apartment-rentals/rideau-place')
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find span classes containing the names of the suite types
    for i in page_parsed.findAll('span', attrs={'class', 'suite-type title'}):
        suite_types.append(i.text.strip())

    # find span classes containing the rental rates for said suite types
    for j in page_parsed.findAll('span', 'value title'):
        suite_rental_rates.append(j.text.strip()[1:])

    # find the <a> tags containing the 'Inquire' button, we can assume anything
    # else would not have any vacancies
    for v in page_parsed.findAll('a', 'open-suite-modal secondary-button'):
        if v.text.strip() == 'Inquire':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    # iterate thru suite_types and suite_rental_rates to create the rideau_suite_min dictionary
    for unit in suite_types:
        _rate = suite_rental_rates.pop(0)
        rideau_suite_min[unit] = _rate

    #print(rideau_suite_min, is_vacant)
    return rideau_suite_min, is_vacant

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

def park_place_south():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of portofino.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    parkplace_suite_min = dict()
    suite_types = ['maple', 'willow', 'cotton', 'pine']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/park-place-south/floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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

    # the maple
    maple = script_list[0]
    maple = maple[148:-212]
    maple = maple.split()
    #print(maple)

    # the willow
    willow = script_list[2]
    willow = willow[148:-212]
    willow = willow.split()

    # the cotton
    cotton = script_list[4]
    cotton = cotton[150:-212]
    cotton = cotton.split()

    # the pine
    pine = script_list[6]
    pine = pine[154:-16]
    pine = pine.split()

    # order rental rates into list + vacancy numbers from 'availableCount:'
    rental_rates_min = [maple[5], willow[5], cotton[5], pine[5]]
    is_vacant = [maple[7], willow[7], cotton[7], pine[7]]

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
        parkplace_suite_min[unit] = rent

    #print(parkplace_suite_min, is_vacant_final)
    return parkplace_suite_min, is_vacant_final


def pineridge():
    """First complete property updater script as of April 2022. 
    Considering this a rough draft until all other properties for the other
    sheets in Alberta are created, and followed through testing of a few months
    throughout the year. 
    
    Since these scripts involve webscraping to gather such a small but albeit
    specific range of information, I expect these to eventually be 
    rewritten to be more readily and easily maintained by someone other 
    than myself simply because I believe that some of the competitors will 
    sell the property to a different company and/or change the general 
    structure of their property website in general.
    
    For Version 1.0-Pineridge_grabber.py, 'body div.row.property-unit' table is
    parsed and split into a list of lists (suite_info), each list containing 
    information regarding each unique unit type. For loops are used to 
    traverse the list of lists (suite_info) to pickout general information 
    pertaining to the current unit type we are looking for.
    

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = pineridge(); print(d, x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)

    Vars:
        pineridge_pg = Grabs the HTML link for the Pineridge apartments owned
                       har-par.
        pineridge_soup = BeautifulSoup call to parse the pineridge website.

        pr_suite_types (list) = list to hold the types of units pineridge 
                                provides. They will be placed into 
                                pineridge_rents alongside the rent rate per unit
                                
        pr_suite_desc(str)= pineridge_soup.select('body div.row.property-unit')
                            to retrieve the panel holding all the information
                            regarding the unit types, rent rates + info of units
        
        suite_info (list) = list to hold the information gathered from
                            pr_suite_desc. 
 
    Returns:
        pineridge_rents (dictionary) = holds unit types + rent rates for each
                                       unit type.
        is_vacant (list) = list of booleans to represent which unit type
                           has available vacancies or not."""
    pineridge_rents = dict()
    pr_suite_types = []
    is_vacant = []
    suite_info = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    pine_r = requests.get('http://har-par.com/properties.php?PropertyID=141')
    pineridge_soup = BeautifulSoup(pine_r.content, 'html.parser')
    pr_suite_desc = pineridge_soup.select('body div.row.property-unit')

    for suite in pr_suite_desc:
        suite_info.append(suite.text.replace('\n', ' ').split())

    # counter for creating the dictionary of rent rates per unit unit type
    count = 0
    for data in suite_info:
        # WAITLISTING for vacancy is not an option at pineridge currently
        # 'No', 'Vacancy'] ~ No vacant units
        if data[-1] == 'Vacancy':
            is_vacant.append(False)
        # 'Vacancy', 'Apply'] ~ Vacant units for this type of unit
        if data[-1] == 'Apply':
            is_vacant.append(True)
        # for looping through the current list in the list of lists (suite_info)
        for info in data:
            # add bachelor to the types of suites
            if data[0] == 'Bachelor' and len(pr_suite_types) == 0:
                pr_suite_types.append(data[0])
                data.remove(info)
            # removes odd $xxxrent elements from a list
            if info[0] == '$' and info[-1] == 't':
                data.remove(info)
                continue
            # removes monetary list elements that are deposits or not rent specific
            if info[0] == '$' and int(info[1:]) < 698:
                data.remove(info)
                continue
            # add the different types of suits to the list; noted as 1 bedroom,
            # 2 bedroom etc as the first 2 elements of the list for that unit type
            if data[0].isnumeric():
                if data[1].isalpha():
                    new_type = str(data[0]) + f' {data[1]}'
                    pr_suite_types.append(new_type)
                    data.remove(info)
            # add descriptor den to the unit type that advertises having a den
            if info == 'Den':
                pr_suite_types[-1] = pr_suite_types[-1] + ' + Den'
                data.remove(info)
            # add descriptor loft to the unit type that advertises having a loft
            if info == 'loft':
                pr_suite_types[-1] = '1 bedroom + loft'
                data.remove(info)
            # creates dictionary key: value with the found rent value corresponding
            # to the type of unit from pr_suite_types
            # and removes '$' from the actual rental rate
            if info[0] == '$':
                pineridge_rents[pr_suite_types[count]] = info[1:]
                data.remove(info)
                # updating the counter to keep up with the pr_suite_types index
                count += 1

    reordered_rents = dict()
    reordered_rents['Bachelor'] = pineridge_rents['Bachelor']
    reordered_rents['1 Bedroom'] = pineridge_rents['1 Bedroom']
    reordered_rents['1 bedroom + loft'] = pineridge_rents['1 bedroom + loft']
    reordered_rents['2 Bedrooms'] = pineridge_rents['2 Bedrooms']
    reordered_rents['2 Bedrooms + Den'] = pineridge_rents['2 Bedrooms + Den']

    is_vacant_reordered = [is_vacant[0], is_vacant[1], is_vacant[4],
                           is_vacant[2], is_vacant[3]]

    #print(reordered_rents)
    #print(pineridge_rents, is_vacant)
    return reordered_rents, is_vacant_reordered

def fairmont_village():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = fairmont_village(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        fairmont_suite_min (dict)   - unit type: rental rate << formatting of min rate dictionary
        fairmont_suite_max (dict)   - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], [], []]
    suite_types = [[], [], [], []]
    url = 'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/Fairmont-Village/'
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

    card_list, is_vacant = get_vacancies_fairmont(
        temp_card_list, is_vacant, suite_types)
    fairmont_suite_min, fairmont_suite_max = get_rates_fairmont(
        card_list, suite_types)
    #print(fairmont_suite_min, fairmont_suite_max); print(is_vacant)
    return fairmont_suite_min, fairmont_suite_max, is_vacant


def get_vacancies_fairmont(temp_card_list, is_vacant, suite_types):
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


def get_rates_fairmont(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    fairmont_suite_min = dict()
    fairmont_suite_max = dict()
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
        fairmont_suite_min[unit] = min_rate
        fairmont_suite_max[unit] = max_rate
    return fairmont_suite_min, fairmont_suite_max


def meadowview_manor():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of pineridge_grabber.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = meadowview_manor(); print('Rental rates:', d, '\n', c '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        meadowview_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        meadowview_suite_max (dict) - unit type: rental rate << formatting of max rate dictionary
        is_vacant (list)            - list of booleans/ints whether the unit has vacancy or not
        suite_types (list)          - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates_min (list)     - '$xxx' rental rates per suite
        rental_rates_max (list)     - '$xxx' rental rates per suite'''
    is_vacant = [[], [], []]
    suite_types = [[], [], []]
    page = requests.get(
        'https://www.bwalk.com/en-CA/Rent/Details/Alberta/Edmonton/Meadowview-Manor/')
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

    card_list, is_vacant = get_vacancies_meadowview(
        temp_card_list, is_vacant, suite_types)
    meadowview_suite_min, meadowview_suite_max = get_rates_meadowview(
        card_list, suite_types)
    #print(meadowview_suite_min, meadowview_suite_max); print(is_vacant)
    return meadowview_suite_min, meadowview_suite_max, is_vacant


def get_vacancies_meadowview(temp_card_list, is_vacant, suite_types):
    """Grab the status on suite vacancy and the names of the suite types"""
    card_list = [[], [], []]
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
    return card_list, is_vacant


def get_rates_meadowview(temp_card_list, suite_types):
    """Grab the min/max rental rates per suite type"""
    rental_rates_min = []
    rental_rates_max = []
    meadowview_suite_min = dict()
    meadowview_suite_max = dict()
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
        meadowview_suite_min[unit] = min_rate
        meadowview_suite_max[unit] = max_rate
    return meadowview_suite_min, meadowview_suite_max


if __name__ == '__main__':
    pass