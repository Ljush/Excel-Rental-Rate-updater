import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def richmond_arms():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = richmond_arms(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    rich_min = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.har-par.com/properties.php?PropertyID=132'
    unico = 'http://www.har-par.com/properties.php?PropertyID=133'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('h4', 'media-heading'):
        suite_types.append(i.text)
    #print(suite_types)

    # grab rental rates per suite type
    for j in page_parsed.findAll('li'):
        if j.text[:4] == 'Rent' and j.text[-1].isdigit():
            rent_rate = j.text[-4:]
            if rent_rate[0] == '$':
                rent_rate = rent_rate[1:]
                rental_rates_min.append(rent_rate)
            else:
                rental_rates_min.append(rent_rate)

    for x in page_parsed.findAll('div', 'col-xs-3 stat text-center'):
        temp = x.text.split()
        if temp[0] == 'No':
            is_vacant.append(False)
        else:
            is_vacant.append(True)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rich_min[unit] = rate_min

    #print(rich_min, is_vacant)
    return rich_min, is_vacant

if __name__ == '__main__':
    richmond_arms()