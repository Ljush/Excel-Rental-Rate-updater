import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def avalon_court():
    '''If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, x = avalon_court(); print('Rental rates:', d, '\nVacancies:', x)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    avalon_min = dict()
    avalon_max = dict()
    is_vacant = []
    suite_types = []
    rental_rates_min = []
    rental_rates_max = []

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    url = 'http://www.avenueliving.ca/apartments-for-rent/avalon-court'
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab suite types
    for i in page_parsed.findAll('div', 'suite-type cell'):
        suite_types.append(i.text.strip()[8:])

    # grab rental rates per suite type
    for j in page_parsed.findAll('div', 'suite-rate cell'):
        temp_ = j.text.strip()
        temp_ = temp_[1:]
        temp_list = temp_.split('-')
        if len(temp_list) > 1:
            max_rate = temp_list[1]
            max_rate = max_rate[1:]
            rental_rates_min.append(temp_list[0])
            rental_rates_max.append(max_rate)
        else:
            rental_rates_min.append(temp_list[0])
            rental_rates_max.append(temp_list[0])

    for x in page_parsed.findAll('div', 'suite-availability cell'):
        temp = x.text.strip()
        temp = temp.replace('\n', '')
        if temp == 'Book a Showing':
            is_vacant.append(True)
        else:
            is_vacant.append(False)

    for unit in suite_types:
        rate_min = rental_rates_min.pop(0)
        rate_max = rental_rates_max.pop(0)
        avalon_min[unit] = rate_min
        avalon_max[unit] = rate_max

    #print(avalon_min, avalon_max, is_vacant)
    return avalon_min, avalon_max, is_vacant

if __name__ == '__main__':
    avalon_court()