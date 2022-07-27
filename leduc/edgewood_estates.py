import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def edgewood_estates():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of portofino.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    edgewood_suite_min = dict()
    suite_types = ['Meadow', 'Woodland', 'Briar']
    is_vacant = []
    url = 'https://alberta.weidner.com/apartments/ab/leduc/edgewood-estates/floorplans'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    script = park_scripts[63].text[292:-1500]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    script_list = script.split('}')
    #print(script_list)

    # meadow
    meadow = script_list[0]
    meadow = meadow[145:-205]
    meadow = meadow.split()
    #print(meadow)
    
    # woodland
    woodland = script_list[2]
    woodland = woodland[148:-205]
    woodland = woodland.split()
    #print(woodland)
    
    # briar
    briar = script_list[4]
    briar = briar[145:-130]
    briar = briar.split()
    #print(briar)

    rental_rates_min = [meadow[5], woodland[5], briar[5]]
    is_vacant = [meadow[7], woodland[7], briar[7]]

    # remove flaoting zeroes, commas, and dollar signs from string elements of rental_rates_min
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
        edgewood_suite_min[unit] = rent

    #print(edgewood_suite_min, is_vacant_final)
    return edgewood_suite_min, is_vacant_final
    
if __name__ == '__main__':
    edgewood_estates()