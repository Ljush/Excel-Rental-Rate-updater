import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def amblewood_terrace():
    """ If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x, c = amblewood_terrace(); print('min', d); print('max', x); print('vacancy', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)
    Vars:
    amble_suites_min (dict) - Minimum rates + unit types 
    amble_suites_max (dict) - Maximum rates + unit types 
    is_vacant (list)           - List of Bools for whether unit has vacancies
    
    page - calls .get() from requests to grab the webpage
    page_parsed - parses page with BeautifulSoup for the webpage content
    
    find_vacancies_tab - .find() to grab specific class information from page (vacancy information)
    vacancy_box_data - uses findAll() to grab more specific information from find_vacancies_tab
    suite - see find_vacancies_tab; (suite and rent information)
    rents - see vacancy_box_data;
    
    Returns: >> See vars for more info
            amble_suites_min, amble_suites_max, is_vacant"""

    amble_suites_min = dict()
    amble_suites_max = dict()
    suite_types = []
    min_rates = []
    max_rates = []
    is_vacant = []
    url = 'https://www.parabelle.com/apartments/8103-29-ave-amblewood-ter/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('span', 'suite-type'):
        suite_types.append(i.text)

    # find suite rental rates
    for j in page_parsed.findAll('span', 'suite-rate'):
        temp = j.text.strip().split()
        min_ = temp[0]
        min_ = min_[1:]
        
        max_ = temp[-1]
        max_ = max_[1:]
        
        if max_[1] == ',':
            max_ = max_[0:1] + max_[2:]
        if min_[1] == ',':
            min_ = min_[0:1] + min_[2:]
        min_rates.append(min_)
        max_rates.append(max_)

    # find suite vacancy status
    for x in page_parsed.findAll('a', 'open-suite-modal accessible-modal'):
        if x.text == 'Notify me':
            is_vacant.append(False)
        else:
            is_vacant.append(True)
            
    # build dictionary of rental rates per suite type
    for unit in suite_types:
        _min = min_rates.pop(0)
        _max = max_rates.pop(0)
        amble_suites_min[unit] = _min
        amble_suites_max[unit] = _max
        
    #print(amble_suites_min, amble_suites_max, is_vacant)
    return amble_suites_min, amble_suites_max, is_vacant

if __name__ == '__main__':
    amblewood_terrace()