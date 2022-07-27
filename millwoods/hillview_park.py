import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def hillview_park():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = hillview_park(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    hillview_min = dict()
    is_vacant = [False, False]
    suite_types = ['1 Bedroom', '2 Bedroom']
    rental_rates_min = ['0', '0']
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.aimrealestate.ca/b/20173529310000422506'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab rent range
    rent_data_list = []
    for j in page_parsed.findAll('a', 'apartment-view-potential'):
        element = j.text
        element = element.replace('\n', ' ')
        element = element.strip()
        element = element.split()
        rent_data_list.append(element)

    for x in rent_data_list:
        """ Template of resulting suite card row from website
        ['207', '$1,050', '--', '2', '1', 'Available', 'Now!']"""
        # 2 bedroom
        if x[3] == '2':
            rate = x[1]
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            rental_rates_min[1] = rate
            is_vacant[1] = True

        # 1 bedroom
        if x[3] == '1':
            rate = x[1]
            rate = rate.replace('$', '')
            rate = rate.replace(',', '')
            rental_rates_min[0] = rate
            is_vacant[0] = True

    # build min rate dictionary from rental_rates_min
    for unit in suite_types:
        temp = rental_rates_min.pop(0)
        hillview_min[unit] = temp

    #print(hillview_min, is_vacant)
    return hillview_min, is_vacant

if __name__ == '__main__':
    hillview_park()