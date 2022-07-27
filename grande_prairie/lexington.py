import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def lexington():
    lex_suite_min = dict()
    is_vacant = [[], [], []]
    rental_rates_min = [[], [], []]
    suite_types = ['Sheridan', 'Renaissance', 'Legacy']
    url = 'https://www.nalgp.com/properties/9-the-lexington'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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
    
if __name__ == '__main__':
    lexington()