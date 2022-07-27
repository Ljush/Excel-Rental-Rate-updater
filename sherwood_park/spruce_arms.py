import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''

def spruce_arms():
    url = 'https://www.avenueliving.ca/apartments-for-rent/spruce-arms'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    is_vacant = [False, False, False, False, False, False]
    suite_types = ['1 Bedroom', '1 Bedroom Premium', '2 Bedroom',
                   '2 Bedroom Premium', '3 Bedroom', '3 Bedroom Premier']
    
    spruce_min_rates = dict()
    spruce_max_rates = dict()
    
    # extract data about the one bedrooms
    suite_rows_one = page_parsed.findAll('div', attrs={'data-bed-filter': 1})
    one_beds = []
    for one in suite_rows_one:
        element = one.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_one = element.split()
        one_beds.append(element_list_one[7:])

    # extract data about the two bedrooms
    suite_rows_two = page_parsed.findAll('div', attrs={'data-bed-filter': 2})
    two_beds = []
    for two in suite_rows_two:
        element = two.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_two = element.split()
        two_beds.append(element_list_two[7:])

    # extract data about the three bedrooms
    suite_rows_three = page_parsed.findAll('div', attrs={'data-bed-filter': 3})
    three_beds = []
    for three in suite_rows_three:
        element = three.text
        element = element.replace('\n', ' ')
        element = element.replace('\t', ' ')
        element = element.replace('\xa0', '')
        element_list_three = element.split()
        three_beds.append(element_list_three[7:])

    temp_min_rates = [[], [], [], [], [], []]
    temp_max_rates = [[], [], [], [], [], []]
    # one bedrooms
    for index_one, i in enumerate(one_beds):
        # 1 bedroom classic
        if i[0][0] == '$' and index_one == 0:
            temp_min_rates[0] = i[0]
        if i[2][0] == '$' and index_one == 0:
            temp_max_rates[0] = i[2]
        if 'Available' in i or 'Book' in i and index_one == 0:
            is_vacant[0] = True

        # 1 bedroom premium
        if i[0][0] == '$' and index_one == 1:
            temp_min_rates[1] = i[0]
        if i[2][0] == '$' and index_one == 1:
            temp_max_rates[1] = i[2]
        if 'Available' in i or 'Book' in i and index_one == 1:
            is_vacant[1] = True

    # two bedrooms
    for index_two, j in enumerate(two_beds):
        # 2 bedroom classic
        if j[0][0] == '$' and index_two == 0:
            temp_min_rates[2] = j[0]
        if j[2][0] == '$' and index_two == 0:
            temp_max_rates[2] = j[2]
        if 'Available' in j or 'Book' in j and index_two == 0:
            is_vacant[2] = True

        # 2 bedroom premium
        if j[0][0] == '$' and index_two == 1:
            temp_min_rates[3] = j[0]
        if j[2][0] == '$' and index_two == 1:
            temp_max_rates[3] = j[2]
        if 'Available' in j or 'Book' in j and index_two == 1:
            is_vacant[3] = True

    # three bedrooms
    for index_three, k in enumerate(three_beds):
        # 3 bedroom classic
        if k[0][0] == '$' and index_three == 0:
            temp_min_rates[4] = k[0]
        if k[2][0] == '$' and index_three == 0:
            temp_max_rates[4] = k[2]
        if 'Available' in k or 'Book' in k and index_three == 0:
            is_vacant[4] = True

        # 3 bedroom premium
        if k[0][0] == '$' and index_three == 1:
            temp_min_rates[5] = k[0]
        if k[2][0] == '$' and index_three == 1:
            temp_max_rates[5] = k[2]
        if 'Available' in k or 'Book' in k and index_three == 1:
            is_vacant[5] = True
    
    rental_rates_min, rental_rates_max = remove_commas(temp_min_rates, temp_max_rates)

    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        max_rate = rental_rates_max.pop(0)
        spruce_min_rates[unit] = min_rate
        spruce_max_rates[unit] = max_rate

    #print(spruce_min_rates, spruce_max_rates, is_vacant)
    return spruce_min_rates, spruce_max_rates, is_vacant


def remove_commas(temp_min_rates, temp_max_rates):
    rental_rates_min = [[], [], [], [], [], []]
    rental_rates_max = [[], [], [], [], [], []]
    # remove $ and commas from rent rates
    for index_min, x in enumerate(temp_min_rates):
        if x == []:
            rental_rates_min[index_min] = '0'
            continue
        min_ = x
        min_ = min_.replace('$', '')
        min_ = min_.replace(',', '')
        rental_rates_min[index_min] = min_

    # remove $ and commas from rent rates
    for index_max, y in enumerate(temp_max_rates):
        if y == []:
            rental_rates_max[index_max] = '0'
            continue
        max_ = y
        max_ = max_.replace('$', '')
        max_ = max_.replace(',', '')
        rental_rates_max[index_max] = max_
    return rental_rates_min, rental_rates_max

if __name__ == '__main__':
    spruce_arms()