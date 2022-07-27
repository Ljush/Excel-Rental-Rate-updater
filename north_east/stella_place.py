import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def stella_place():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = stella_place(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    stella_min = dict()
    is_vacant = [False, False]
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = [[], []]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.stellaplace.ca/floorplans.aspx?web=1&wdLOR=cA9FBD4BD-1925-3941-8134-89F7F5BEB899'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    suite_card_list = []
    # grab data per suite card/type
    for i in page_parsed.findAll('div', 'span6'):
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\r', ' ')
        element = element.strip()
        element_list = element.split()
        if element_list == []:
            continue
        else:
            suite_card_list.append(element_list)

    # go thru data and extract rental rates/vacancy status
    """ Template of returning suite_card_list (June 13/2022)
['1', 'Bedroom', '(Contact', 'for', 'Availability)', 'Bed', '1', 'Bath', '1', 'Sq.Ft.648', 'Rent', 'Call', 'for', 'Details', 'Specials', 'Deposit', 'Contact', 'Us', '►']
['2', 'Bedroom', '(Available)', 'Bed', '2', 'Bath', '2', 'Sq.Ft.884', '-to', '934', 'Rent', '$1,500', 'Specials', 'Deposit', 'Available', '►']"""
    temp_rents = [[], []]
    for j in suite_card_list:
        #print(j)
        # 1 bedroom
        if j[0] == '1':
            if 'Call' in j:
                temp_rents[0] = '0'
            else:
                temp_rents[0] = j[11]
                is_vacant[0] = True

        # 2 bedroom
        if j[0] == '2':
            if 'Call' in j:
                temp_rents[1] = 0
            else:
                temp_rents[1] = j[11]
                is_vacant[1] = True

    # remove commas from rental rates;
    for index, m in enumerate(temp_rents):
        rent = m
        rent = rent.replace(',', '')
        rent = rent.replace('$', '')
        rental_rates_min[index] = rent


    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        stella_min[unit] = rate

    #print(stella_min, is_vacant)
    return stella_min, is_vacant

if __name__ == '__main__':
    stella_place()