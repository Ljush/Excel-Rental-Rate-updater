import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def park_square():
    park_suite_min = dict()
    is_vacant = []
    # no names given per suite type, sqft shouldn't change (?)
    suite_types = ['850 sqft', '960 sqft', '1050 sqft']
    rental_rates_min = []
    url = 'https://www.quadrealres.com/apartments/ab/edmonton/park-square-6/floorplans'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    park_scripts = page_parsed.findAll('script')
    # isolate script 62 that contains information for each suite card on the website
    script = park_scripts[61].text[292:-1500]
    script = script.replace('\n', '')
    script = script.replace('\t', '')
    script = script.replace('\r', '')
    script = script.strip()
    script_list = script.split('}')

    # two bedroom -> 850 sqft (small)
    small = script_list[0]
    small = small[148:-230]
    small = small.split()
    #print(small)

    # two bedroom -> 960 sqft (medium)
    medium = script_list[2]
    medium = medium[150:-230]
    medium = medium.split()
    #print('\n', medium)

    # two bedroom -> 1050 sqft (large)
    large = script_list[4]
    large = large[155:-40]
    large = large.split()
    #print('\n', large)

    # order rental rates + vacancy status/numbers according to the spreadsheet
    temp_rates = [small[5], medium[5], large[5]]
    #print(temp_rates)
    

    # remove floating zeroes, commas, and dollar signs from the list elements (str)
    for i in temp_rates:
        i = i.replace('"', '')
        i = i.replace('$', '')
        i = i.replace(',', '')
        i = i[:-3]
        rental_rates_min.append(i)
    """
    # remove commas from vacancy status
    temp_vacancy = [small[7], medium[7], large[7]]
    for j in temp_vacancy:
        j = j.replace(',', '')
        is_vacant.append(j)
    """

    """July 26/2022 - studio + 2b + 2b + 2b
        [497 sqft, 850 sqft, 960 sqft, 1050 sqft] """
    for x in rental_rates_min:
        if x == 0:
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    # build rental rate dictionary
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        park_suite_min[unit] = rate

    #print(park_suite_min, is_vacant)
    return park_suite_min, is_vacant
    

if __name__ == '__main__':
    park_square()