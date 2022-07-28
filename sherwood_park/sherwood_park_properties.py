# sherwood_park_properties.py
import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/
Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def aspen_park():
    '''

        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = aspen_village(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    aspen_min_rates = dict()
    aspen_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info']
    suite_types = ['Aspen', 'Birch', 'Cottonwood', 'Dogwood']
    url = 'https://rentsherwoodpark.com/apartments-for-rent/4-augustine-crescent-Sherwood-Park-AB-33573/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    page_info = page_parsed.findAll('div', 'col-sm-2 col-xs-3')#'panel panel-default')

    """Extract rental rates per suite type; we will only use the rental rates for
    the types noted in suite_types above."""
    # min/max rate lists temporary to later select specific rents according to suite_types
    temp_min = []
    temp_max = []
    for i in page_info:
        temp = i.text
        temp = temp.replace('\n', '')
        temp = temp.replace('\t', '')
        temp = temp.strip()
        # split the PRICE string into a list
        if temp[0] == 'P':
            temp_list = temp.split()
            temp_list = temp_list[1:]
            min_rate_temp = temp_list[0].replace('$', '')
            max_rate_temp = temp_list[-1].replace('$', '')
            temp_min.append(min_rate_temp)
            temp_max.append(max_rate_temp)

    # reassign rental rates in accordance to suite_types list in prep for the dict creation
    rental_rates_min = [temp_min[0], temp_min[2], temp_min[5], temp_min[7]]
    rental_rates_max = [temp_max[0], temp_max[2], temp_max[5], temp_max[7]]

    # build the min/max dictionaries
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        aspen_min_rates[unit] = min_rate
        aspen_max_rates[unit] = max_rate

    #print(aspen_min_rates, aspen_max_rates, is_vacant)
    return aspen_min_rates, aspen_max_rates, is_vacant


def emerald_hills():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = emerald_hills(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    emerald_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.skylineliving.ca/en/apartments/alberta/sherwood-park/5600-clover-bar-rd-sherwood-park-ab'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rental rates
    for i in page_parsed.findAll('span', 'property-types-rent__starting-at'):
        temp = i.text[12] + i.text[14:17]
        rental_rates_min.append(temp)

    # website doesn't directly state available vacancies, will assume 'No Info'
    for j in range(len(suite_types)):
        is_vacant.append('No Info')

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        emerald_min[unit] = temp_

    #print(emerald_min, is_vacant)
    return emerald_min, is_vacant


def greenwood_village():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = greenwood_village(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    greenwood_min_rates = dict()
    greenwood_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info']
    suite_types = ['2 Bedroom', '2 Bedroom Elite',
                   '3 Bedroom', '3 Bedroom Elite']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://greatapartments.ca/mha_property/greenwood-village/'
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

    # clean up rental rates strings, split into list and extract the rental rate
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
        greenwood_min_rates[unit] = min_
        greenwood_max_rates[unit] = max_

    """This murray hill property specifically does not report max rates for their
    suite types so we won't return them for now"""
    #print(greenwood_min_rates, greenwood_max_rates, is_vacant)
    #print(greenwood_min_rates, is_vacant)
    return greenwood_min_rates, is_vacant


def harmony_market():
    '''
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = harmony_market(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
        No max rates for rideau place right now!
        harmony_suite_min (dict) - unit type: rental rate << formatting of min rate dictionary
        is_vacant (list)           - list of booleans whether the unit has vacancy or not
        suite_types (list)         - bachelor, 1 bed, 2 bed, 3 bed etc.
        rental_rates(list)         - '$xxx' rental rates per suite'''
    harmony_suite_min = dict()
    #harmony_suite_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates = []
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    url = 'https://www.mmgltd.com/apartment-rentals/harmony-at-the-market'
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

    # iterate thru suite_types and rental_rates to create the harmony_suite_min dictionary
    for unit in suite_types:
        temp = rental_rates.pop(0)
        harmony_suite_min[unit] = temp

    #print(harmony_suite_min, is_vacant)
    return harmony_suite_min, is_vacant


def spruce_arms():
    url = 'https://www.avenueliving.ca/apartments-for-rent/spruce-arms'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    is_vacant = [False, False, False, False, False, False]
    suite_types = ['1 Bedroom', '1 Bedroom Premium', '2 Bedroom',
                   '2 Bedroom Premium', '3 Bedroom', '3 Bedroom Premier']

    spruce_min_rates = dict()
    spruce_max_rates = dict()

    # extract data about the one bedrooms
    suite_rows_one = page_parsed.findAll('div', attrs={'data-bed-filter': 1})
    one_beds = []
    for one in suite_rows_one:
        element = one.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_one = element.split()
        one_beds.append(element_list_one[7:])

    # extract data about the two bedrooms
    suite_rows_two = page_parsed.findAll('div', attrs={'data-bed-filter': 2})
    two_beds = []
    for two in suite_rows_two:
        element = two.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_two = element.split()
        two_beds.append(element_list_two[7:])

    # extract data about the three bedrooms
    suite_rows_three = page_parsed.findAll('div', attrs={'data-bed-filter': 3})
    three_beds = []
    for three in suite_rows_three:
        element = three.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_three = element.split()
        three_beds.append(element_list_three[7:])

    temp_min_rates = [[], [], [], [], [], []]
    temp_max_rates = [[], [], [], [], [], []]
    # one bedrooms
    for index_one, i in enumerate(one_beds):
        # 1 bedroom classic
        if i[0][0] == '$' and index_one == 0:
            temp_min_rates[0] = i[0]
        if i[2][0] == '$' and index_one == 0:
            temp_max_rates[0] = i[2]
        if 'Available' in i or 'Book' in i and index_one == 0:
            is_vacant[0] = True

        # 1 bedroom premium
        if i[0][0] == '$' and index_one == 1:
            temp_min_rates[1] = i[0]
        if i[2][0] == '$' and index_one == 1:
            temp_max_rates[1] = i[2]
        if 'Available' in i or 'Book' in i and index_one == 1:
            is_vacant[1] = True

    # two bedrooms
    for index_two, j in enumerate(two_beds):
        # 2 bedroom classic
        if j[0][0] == '$' and index_two == 0:
            temp_min_rates[2] = j[0]
        if j[2][0] == '$' and index_two == 0:
            temp_max_rates[2] = j[2]
        if 'Available' in j or 'Book' in j and index_two == 0:
            is_vacant[2] = True

        # 2 bedroom premium
        if j[0][0] == '$' and index_two == 1:
            temp_min_rates[3] = j[0]
        if j[2][0] == '$' and index_two == 1:
            temp_max_rates[3] = j[2]
        if 'Available' in j or 'Book' in j and index_two == 1:
            is_vacant[3] = True

    # three bedrooms
    for index_three, k in enumerate(three_beds):
        # 3 bedroom classic
        if k[0][0] == '$' and index_three == 0:
            temp_min_rates[4] = k[0]
        if k[2][0] == '$' and index_three == 0:
            temp_max_rates[4] = k[2]
        if 'Available' in k or 'Book' in k and index_three == 0:
            is_vacant[4] = True

        # 3 bedroom premium
        if k[0][0] == '$' and index_three == 1:
            temp_min_rates[5] = k[0]
        if k[2][0] == '$' and index_three == 1:
            temp_max_rates[5] = k[2]
        if 'Available' in k or 'Book' in k and index_three == 1:
            is_vacant[5] = True

    rental_rates_min, rental_rates_max = remove_commas_spruce(
        temp_min_rates, temp_max_rates)

    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        spruce_min_rates[unit] = min_rate
        spruce_max_rates[unit] = max_rate

    #print(spruce_min_rates, spruce_max_rates, is_vacant)
    return spruce_min_rates, spruce_max_rates, is_vacant


def remove_commas_spruce(temp_min_rates, temp_max_rates):
    rental_rates_min = [[], [], [], [], [], []]
    rental_rates_max = [[], [], [], [], [], []]
    # remove $ and commas from rent rates
    for index_min, x in enumerate(temp_min_rates):
        if x == []:
            rental_rates_min[index_min] = '0'
            continue
        min_ = x
        min_ = min_.replace('$', '')
        min_ = min_.replace(',', '')
        rental_rates_min[index_min] = min_

    # remove $ and commas from rent rates
    for index_max, y in enumerate(temp_max_rates):
        if y == []:
            rental_rates_max[index_max] = '0'
            continue
        max_ = y
        max_ = max_.replace('$', '')
        max_ = max_.replace(',', '')
        rental_rates_max[index_max] = max_
    return rental_rates_min, rental_rates_max


def stonebridge():
    '''As of June 14/2022; website incorrectly redirects you when clicking on a 
    suite card; unclear about vacancy status and whether or not the rates are accurate

        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = stonebridge(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    stone_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '1 Bedroom +', '2 Bedroom', '3 Bedroom']
    rental_rates_min = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    one_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=1'
    #two_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=2'
    #three_url = 'https://www.olcl.ca/properties/cities/sherwood-park?minBeds=3'

    page_one = requests.get(one_url, headers=headers)
    #page_two = requests.get(two_url, headers=headers)
    #page_three = requests.get(three_url, headers=headers)

    page_one_parsed = BeautifulSoup(page_one.content, 'html.parser')

    # grab suite data about suite types and place the data into a list
    # grabbed from the 'properties' drop down section of the website since it currently is very broken and does not
    # redirect correctly when you click on any type of suite under this property
    for i in page_one_parsed.findAll('div', 'city'):
        temp = i.text
        temp = temp.replace('\n', '')
        temp = temp.replace('\t', ' ')
        temp = temp.strip()
        city_list = temp.split()
        if city_list[0] == 'Sherwood':
            sherwood_list = (city_list[2:])

    # remove all instances of the word 'from' from the sherwood list, making it easier to work with
    for element in sherwood_list:
        if element == 'from':
            sherwood_list.remove(element)

    # not yet sure (june 14 2022) that 1 bed premium would show as '1+' or '1 bed premium'
    suite_list_check = ['1', '1+']

    # assign rates per suite to temporary dictionary
    temp_final_dict = dict()
    for j in sherwood_list:
        # 1 bed
        if j[0] == '1':
            current_type = j
            if current_type not in temp_final_dict.keys():
                current_type += '+'
            continue
        # 2 bed
        if j[0] == '2':
            current_type = j
            continue
        # 3 bed
        if j[0] == '3':
            current_type = j
            continue
        # add rate to temp dictionary
        if j[0] == '$':
            rate = j
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            temp_final_dict[current_type] = rate
        # check for all 4 suite types to be in the temp dictionary;
        # if a suite type is not in the temp dictionary, add it with a rate of '0'
        if len(temp_final_dict) != 4:
            for suite in suite_list_check:
                if suite not in temp_final_dict.keys():
                    temp_final_dict[suite] = '0'

    # move rental rates per suite to rental_rates_min
    for rent_rate in temp_final_dict.values():
        rental_rates_min.append(rent_rate)

    # website doesn't directly state available vacancies, will assume 'No Info'
    for x in range(len(suite_types)):
        is_vacant.append('No Info')

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        stone_min[unit] = temp_

    #print(stone_min, is_vacant)
    return stone_min, is_vacant


def tisbury():
    """Each suite type has its own unique url to display information about that
    suite type"""
    prestwick_url = 'https://sherwoodparkrentals.ca/suites/prestwick-1-bedroom-suite/'
    turnberry_url = 'https://sherwoodparkrentals.ca/suites/turnberry-1-bedroom-suite/'
    oakmont_url = 'https://sherwoodparkrentals.ca/suites/oakmont-2-bedroom-suite/'
    birkdale_url = 'https://sherwoodparkrentals.ca/suites/birkdale-2-bedroom-suite/'

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    prestwick = requests.get(prestwick_url, headers=headers)
    turnberry = requests.get(turnberry_url, headers=headers)
    oakmont = requests.get(oakmont_url, headers=headers)
    birkdale = requests.get(birkdale_url, headers=headers)

    prestwick_parsed = BeautifulSoup(prestwick.content, 'html.parser')
    turnberry_parsed = BeautifulSoup(turnberry.content, 'html.parser')
    oakmont_parsed = BeautifulSoup(oakmont.content, 'html.parser')
    birkdale_parsed = BeautifulSoup(birkdale.content, 'html.parser')

    tisbury_suite_min = dict()
    suite_types = ['1 Bed Prestwick', '1 Bed Turnberry', '2 Bed Oakmont',
                   '2 Bed Birkdale']
    is_vacant = ['No info', 'No Info', 'No Info', 'No Info']
    temp_rates_min = [[], [], [], []]

    # extract rate for prestwick
    for a in prestwick_parsed.findAll('div', 'av_iconlist_title iconlist_title_small'):
        element_p = a.text
        if element_p[0:4] == 'Rent':
            result_p = element_p.split()
            for p in result_p:
                if p[0] == '$':
                    temp_rates_min[0] = p

    # extract rate for turnberry
    for b in turnberry_parsed.findAll('div', 'av_iconlist_title iconlist_title_small'):
        element_t = b.text
        if element_t[0:4] == 'Rent':
            result_t = element_t.split()
            for t in result_t:
                if t[0] == '$':
                    temp_rates_min[1] = t

    # extract rate for oakmont
    for c in oakmont_parsed.findAll('div', 'av_iconlist_title iconlist_title_small'):
        element_o = c.text
        if element_o[0:4] == 'Rent':
            result_o = element_o.split()
            for o in result_o:
                if o[0] == '$':
                    temp_rates_min[2] = o

    # extract rate for birkdale
    for d in birkdale_parsed.findAll('div', 'av_iconlist_title iconlist_title_small'):
        element_d = d.text
        if element_d[0:4] == 'Rent':
            result_d = element_d.split()
            for current in result_d:
                if current[0] == '$':
                    temp_rates_min[3] = current

    # remove $ and commas from rates
    rental_rates_min = [[], [], [], []]
    for index, rental_rate in enumerate(temp_rates_min):
        rate = rental_rate
        rate = rate.replace('$', '')
        rate = rate.replace(',', '')
        rental_rates_min[index] = rate

    # build dictionary of rental rates per suite type
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        tisbury_suite_min[unit] = min_rate

    #print(tisbury_suite_min, is_vacant)
    return tisbury_suite_min, is_vacant


if __name__ == '__main__':
    pass
