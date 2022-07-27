import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def northland():
    land_suite_min = dict()
    is_vacant = [[], [], [], []]
    rental_rates_min = [[], [], [], []]
    suite_types = ['Bachelor', '1 Bedroom', '2 Bedroom', '2 Bedroom 2 Bath']
    url = 'https://www.northlandmanagement.ca/residential-properties/grande-prairie/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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

    # template of suite_card_info (june 16,2022)
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
    
if __name__ == '__main__':
    northland()