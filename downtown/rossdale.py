import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def rossdale():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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

if __name__ == '__main__':
    rossdale()