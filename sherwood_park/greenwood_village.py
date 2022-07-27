import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def greenwood_village():
    '''
    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = greenwood_village(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    greenwood_min_rates = dict()
    greenwood_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info', 'No Info']
    suite_types = ['2 Bedroom', '2 Bedroom Elite', '3 Bedroom', '3 Bedroom Elite']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://greatapartments.ca/mha_property/greenwood-village/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')

    rate_info = page_parsed.findAll('div', 'mb-3')
    temp_rate_list = []
    for g in rate_info:
        if len(temp_rate_list) >= 4:
            break
        rate = g.text
        rate = rate.replace('\n', '')
        rate = rate.strip()
        
        # take only rent rate texts; that are also not deposits
        if rate[0] == '$' and rate[-1] != 't':
            temp_rate_list.append(rate)

    # clean up rental rates strings, split into list and extract the rental rate
    for i in temp_rate_list:
        rent_rate = i
        rent_rate = rent_rate.replace('$', '')
        rent_rate = rent_rate.replace('-', ' ')
        rent_rate = rent_rate.replace(' /mo.', '')
        rent_rate = rent_rate.replace(',', '')
        rent_temp_list = rent_rate.split()
        
        min_rate = rent_temp_list[0]
        max_rate = rent_temp_list[1]
        rental_rates_min.append(min_rate)
        rental_rates_max.append(max_rate)
    
    """Vacancy status is unknown, comment on the availability column
        that only "Book a viewing" is showing per suite type"""

    for unit in suite_types:
        min_ = rental_rates_min.pop(0)
        max_ = rental_rates_max.pop(0)
        greenwood_min_rates[unit] = min_
        greenwood_max_rates[unit] = max_

    """This murray hill property specifically does not report max rates for their
    suite types so we won't return them for now"""
    #print(greenwood_min_rates, greenwood_max_rates, is_vacant)
    #print(greenwood_min_rates, is_vacant)
    return greenwood_min_rates, is_vacant
        
        
if __name__ == '__main__':
    greenwood_village()