import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
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

'''The village on excel may not be in line with the website, i do not know right now
if they just take unavailable units off the website entirely or not. maybe they do 
actually take their website seriously lol,'''
if __name__ == '__main__':
    the_village()