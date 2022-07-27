import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def northgate():
    north_suite_min = dict()
    is_vacant = [False, False]
    rental_rates_min = [[], []]
    suite_types = ['1 Bedroom', '2 Bedroom']
    url = 'https://www.rentnorthview.com/apartments/northgate-iii-northgate-apartments'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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
    
if __name__ == '__main__':
    northgate()