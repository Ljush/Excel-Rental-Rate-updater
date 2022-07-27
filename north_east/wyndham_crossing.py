import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def wyndham_crossing():
    '''
    Follows same general logic to parse information (as park_place) with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.
    '''
    wynd_suite_min = dict()
    suite_types = ['maple', 'willow', 'cotton', 'pine']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/wyndham-crossing/floorplans'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    wynd_scripts = page_parsed.findAll('div', 'accordion-inner')
    for i in wynd_scripts:
        element = i.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', '')
        element = element.strip()
        print(repr(element))
    # isolate script 64 and cut out large parts of the str(script)
    # script = wynd_scripts[63].text[292:-1500]
    # script = script.replace("\n", "")
    # script = script.replace('\t', '')
    # script = script.replace('\r', '')
    # script = script.strip()
    # # since script is extremely long string, split it per '}' into list
    # script_list = script.split('}')
    


    #print(wynd_suite_min, is_vacant_final)
    #return wynd_suite_min, is_vacant_final
    
if __name__ == '__main__':
    wyndham_crossing()