import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def gateway():
    gate_suite_min = dict()
    is_vacant = [False, False, False, False, False]
    rental_rates_min = [[], [], [], [], []]
    suite_types = ['1 Bedroom', '2 Bedroom 668 sqft', '2 Bedroom 780 sqft',
                   '2 Bedroom 799 sqft', '2 Bedroom 825 sqft']
    url = 'https://www.woodsmere.ca/property/gateway-apartments/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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
        
if __name__ == '__main__':
    gateway()