import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def carrington():
    carr_suite_min = dict()
    suite_types = ['Churchill', 'Aberdeen', 'Hudson', 'Pioneer']
    url = 'https://alberta.weidner.com/apartments/ab/grande-prairie/carrington-place/floorplans'
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

    # churchill
    churchill = script_list[0]
    churchill = churchill[148:-212]
    churchill = churchill.split()
    #print(churchill)

    # aberdeen
    aberdeen = script_list[2]
    aberdeen = aberdeen[148:-205]
    aberdeen = aberdeen.split()
    #print(aberdeen)

    #hudson
    hudson = script_list[5]
    hudson = hudson[148:-205]
    hudson = hudson.split()
    #print(hudson)


    #pioneer
    pioneer = script_list[7]
    pioneer = pioneer[148:-12]
    pioneer = pioneer.split()
    #print(pioneer)

    rental_rates_min = [churchill[5], aberdeen[5], hudson[5], pioneer[5]]
    is_vacant = [churchill[7], aberdeen[7], hudson[7], pioneer[7]]

    min_rates_final = []
    for i in rental_rates_min:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        min_rates_final.append(i)

    # remove commas that can appear from 'availableCount' results
    is_vacant_final = []
    for j in is_vacant:
        j = j.replace(',', '')
        is_vacant_final.append(j)

    #build dictionary of rental rates per suite type
    for unit in suite_types:
        rent = min_rates_final.pop(0)
        carr_suite_min[unit] = rent

    #print(carr_suite_min, is_vacant_final)
    return carr_suite_min, is_vacant_final
    
if __name__ == '__main__':
    carrington()