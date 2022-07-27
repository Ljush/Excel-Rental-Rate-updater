import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def macewan_greens():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = macewan_greens(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    macewan_min = dict()
    is_vacant = []
    rental_rates_min = []
    suite_types = []

    url = 'https://www.macewangreens.com/apartments-for-rent/leduc/1-bedroom/6201-grant-macewan-blvd/40875/plan/76679/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental types
    for i in page_parsed.findAll('p', 'col-sm-12 ypnh-propertypage-title-fp'):
        suite_types.append(i.text)
    
    # find suite rental rates
    for j in page_parsed.findAll('span', 'break-two'):
        rental_rates_min.append(j.text[1:-6])

    '''VACANCY STATUS HAS NOT SHOW UP YET MAY 24 2022'''
    # find suite vacancy status
    for k in range(len(suite_types)):
        is_vacant.append('No Info')
        
    # build dictionary of rental rates per suite type
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        macewan_min[unit] = rate
    
    #print(macewan_min, is_vacant)
    return macewan_min, is_vacant


if __name__ == '__main__':
    macewan_greens()