import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def willowbrook():
    willow_suite_min = dict()
    willow_suite_max = dict()
    suite_types = ['Riesling', 'Cabernet', 'Malbec', 'Merlot', 'Shiraz']
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info', 'No Info']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://highstreetliving.ca/locations/grande-prairie-willowbrook/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    # grab the individual suite card data
    suite_cards = page_parsed.findAll('div', 'wpb_wrapper')
    suite_card_list = []
    for i in suite_cards:
        temp = i.text
        temp = temp.replace('\n', ' ')
        temp = temp.replace('\t', ' ')
        temp = temp.strip()
        temp_list = temp.split()
        
        # some lists were empty, or way too long and not what we are looking for
        if len(temp_list) <= 100 and len(temp_list) > 12:
            if temp_list[0] in suite_types:
                    suite_card_list.append(temp_list)

    # extract rental rates min/max
    count = 0
    for j in suite_card_list:
        for k in j:
            # finds specific rate, remove $ and * elements from string
            if k[0] == '$':
                rate = k
                rate = rate.replace('$', '')
                rate = rate.replace('*', '')
                # checking if count is even/odd distinguishes whether rate is 
                # a minimum rate or maximum rate
                if count % 2 == 0:
                    rental_rates_min.append(rate)
                    count += 1
                else:
                    rental_rates_max.append(rate)
                    count += 1

    # build min/max dictionaries with rents to suite types
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        willow_suite_min[unit] = min_rate
        willow_suite_max[unit] = max_rate

    #print(willow_suite_min); print(willow_suite_max); print(is_vacant)
    return willow_suite_min, willow_suite_max, is_vacant
    
if __name__ == '__main__':
    willowbrook()