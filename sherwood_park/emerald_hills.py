import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def emerald_hills():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = emerald_hills(); print('Rental rates:', d, '\nVacancies:',x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    emerald_min = dict()
    is_vacant = []
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.skylineliving.ca/en/apartments/alberta/sherwood-park/5600-clover-bar-rd-sherwood-park-ab'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rental rates
    for i in page_parsed.findAll('span', 'property-types-rent__starting-at'):
        temp = i.text[12] + i.text[14:17]
        rental_rates_min.append(temp)


    # website doesn't directly state available vacancies, will assume 'No Info'
    for j in range(len(suite_types)):
        is_vacant.append('No Info')

    # assign suite types to respective rental rates into a dictionary
    for unit in suite_types:
        temp_ = rental_rates_min.pop(0)
        emerald_min[unit] = temp_

    #print(emerald_min, is_vacant)
    return emerald_min, is_vacant

if __name__ == '__main__':
    emerald_hills()