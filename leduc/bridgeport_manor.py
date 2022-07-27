import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def bridgeport_manor():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = bridgeport_manor(); print('Rental rates:', d, c, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    bridgeport_min = dict()
    bridgeport_max = dict()
    is_vacant = []
    suite_types = ['3 Bed + Den']
    rental_rates_min = []
    rental_rates_max = []

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.greystonermc.ca/residential/bridgeport-manor'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the single rate for this property
    for i in page_parsed.findAll('span', 'suite-rate'):
        rate = i.text.strip()
        min_rate = rate[1:5]
        max_rate = rate[-4:]
        rental_rates_min.append(min_rate)
        rental_rates_max.append(max_rate)

    # grab vacancy status
    for j in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if str(j.text) == 'Available Now':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rate_max = rental_rates_max.pop(0)
        bridgeport_min[unit] = rate_min
        bridgeport_max[unit] = rate_max
        
    
    #print(bridgeport_min, bridgeport_max, is_vacant)
    return bridgeport_min, bridgeport_max, is_vacant

if __name__ == '__main__':
    bridgeport_manor()