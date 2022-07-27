import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def park_place_south():
    '''
    Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    Check documentation of portofino.py for a somewhat more in-depth
    description of how the general process works. Unless the website is fundamentally different
    in some aspect, I don't think it would be difficult to maintain otherwise.
    '''
    parkplace_suite_min = dict()
    suite_types = ['maple', 'willow', 'cotton', 'pine']
    url = 'https://alberta.weidner.com/apartments/ab/edmonton/park-place-south/floorplans'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab script tags from website
    park_scripts = page_parsed.findAll('script')
    # isolate script 64 and cut out large parts of the str(script)
    script = park_scripts[63].text[292:-1500]
    script = script.replace("\n", "")
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    # since script is extremely long string, split it per '}' into list
    script_list = script.split('}')
    
    # the maple
    maple = script_list[0]
    maple = maple[148:-212]
    maple = maple.split()
    #print(maple)
    
    # the willow
    willow = script_list[2]
    willow = willow[148:-212]
    willow = willow.split()

    # the cotton
    cotton = script_list[4]
    cotton = cotton[150:-212]
    cotton = cotton.split()

    # the pine
    pine = script_list[6]
    pine = pine[154:-16]
    pine = pine.split()
    
    # order rental rates into list + vacancy numbers from 'availableCount:'
    rental_rates_min = [maple[5], willow[5], cotton[5], pine[5]]
    is_vacant = [maple[7], willow[7], cotton[7], pine[7]]

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
        parkplace_suite_min[unit] = rent

    #print(parkplace_suite_min, is_vacant_final)
    return parkplace_suite_min, is_vacant_final
    
if __name__ == '__main__':
    park_place_south()