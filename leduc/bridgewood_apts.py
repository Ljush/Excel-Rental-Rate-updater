import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def bridgewood_apts():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = bridgewood_apts(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    bridgewood_min = dict()
    #bridgewood_max = dict()
    is_vacant = []
    suite_types = ['479 sqft', '668 sqft', '799 sqft', '825 sqft', '780 sqft']
    rental_rates_min = []

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'https://www.woodsmere.ca/property/bridgewood-apartments/'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # find suite rental rates
    #for i in page_parsed.findAll('span', 'h2-big'):
       # rental_rates_min.append(i.text[1:-6])
    
    for j in page_parsed.findAll('div', 'col-md-1-4 col-xs-1-2'):
        temp = j.text.split()
        print(temp)
        temp_first_item = temp[0]
        # append rental rate
        if temp_first_item[0] == '$':
            rent_rate = temp_first_item[1:-13]
            rental_rates_min.append(rent_rate)
            continue
        # append waitlist for suite 
        if temp_first_item[0] == 'W':
            is_vacant.append('Waitlist')
            continue
        # append vacancy for suite
        if temp_first_item[0] == 'A':
            is_vacant.append(True)
            continue

    print(rental_rates_min); print(is_vacant)
    if rental_rates_min == []:
        return bridgewood_min, is_vacant
    
    for unit in suite_types:
        rate = rental_rates_min.pop(0)
        bridgewood_min[unit] = rate

    print(bridgewood_min, is_vacant)
    return bridgewood_min, is_vacant

if __name__ == '__main__':
    bridgewood_apts()