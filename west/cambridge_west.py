import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def cambridge_west():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.'''
    cambridge_suite_min = dict()
    suite_types = ['Eton', 'Oxford', 'Windsor']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/cambridge-west/floorplans'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    # isolate script 64 and cut out large parts of the str(script), removing whitespace as well
    script = park_scripts[63].text[292:-1510]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    
    # since script is extremely long string, split it per '}' into list
    script_list = script.split('}')

    # Eton
    eton = script_list[0]
    eton = eton[140:-200]
    eton = eton.split()

    # Oxford
    oxford = script_list[2]
    oxford = oxford[148:-200]
    oxford = oxford.split()

    # Windsor
    windsor = script_list[4]
    windsor = windsor[153:]
    windsor = windsor.split()

    # order rental rates into list + vacancy numbers from 'availableCount:'
    rental_rates_min = [eton[5], oxford[5], windsor[5]]
    is_vacant = [eton[7], oxford[7], windsor[7]]

    # remove floating zeroes, commas and dollar signs from string elements
    rent_rates_final = []
    for i in rental_rates_min:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        rent_rates_final.append(i)
        
    # remove commas that can appear from 'availableCount' results
    is_vacant_final = []
    for j in is_vacant:
        j = j.replace(',', '')
        is_vacant_final.append(j)

    for unit in suite_types:
        rent = rent_rates_final.pop(0)
        cambridge_suite_min[unit] = rent

    #print(cambridge_suite_min, is_vacant_final)
    return cambridge_suite_min, is_vacant_final
    
if __name__ == '__main__':
    cambridge_west()