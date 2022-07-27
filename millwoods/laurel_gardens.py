import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def laurel_gardens():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = laurel_gardens(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    laurel_min = dict()
    #laurel_max = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []
    
    url = 'https://www.broadstreet.ca/residential/laurel-gardens'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
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
        laurel_min[unit] = rate

    #print(laurel_min, is_vacant)
    return laurel_min, is_vacant

if __name__ == '__main__':
    laurel_gardens()