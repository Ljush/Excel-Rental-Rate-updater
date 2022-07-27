import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
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
    tisbury()