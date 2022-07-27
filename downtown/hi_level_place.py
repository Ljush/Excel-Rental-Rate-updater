import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def hi_level_place():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c = hi_level_place(); print('Rental rates:', d, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    level_min_rates = dict()
    suite_types = ['Bachelor', 'Bachelor Renovated', 'One Bedroom',
                   'One Bedroom Renovated', 'Two Bedroom',
                   'Two Bedroom Renovated']
    url = 'https://www.minto.com/edmonton/Edmonton-apartment-rentals/Hi-Level-Place/main.html#rates_floorplans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    table = page_parsed.find(
        'table', 'table table-striped__ table-responsive-minto border-bottom')
    site_data = table.findAll('tr', 'text-center py-3 py-md-0')
    #print(repr(site_data[2].text))
    temp_data_list = []
    for j in site_data:
        data = j.text
        #print(repr(data))
        data = data.replace('\n', ' ')
        data = data.strip()
        temp_name_list = data.split()
        temp_name_list = temp_name_list[:-3]
        #print(temp_name_list)
        temp_data_list.append(temp_name_list)

    rental_rates_min, is_vacant = get_rates(temp_data_list)

    #print(rental_rates_min, is_vacant)
    for unit in suite_types:
        min_rate = rental_rates_min.pop(0)
        if min_rate == []:
            level_min_rates[unit] = '0'
        else:
            level_min_rates[unit] = min_rate

    #print(level_min_rates, is_vacant)
    return level_min_rates, is_vacant


def get_rates(temp_data_list):
    is_vacant = [False, False, False, False, False, False]
    rental_rates_min = [[], [], [], [], [], []]
    suite_data_list = [[], [], [], [], [], []]
    
    for w in temp_data_list:
        #print(w)
        # Bachelor unit
        if w[0] == 'Bachelor' and w[1] != 'Renovated':
            suite_data_list[0] = w
            # determine if the bachelor has vacancy or not
            if 'Available' in suite_data_list[0]:
                is_vacant[0] = True
            if 'Waitlist' in suite_data_list[0]:
                is_vacant[0] = False

            # grab the rate of the bachelor suite
            for element in suite_data_list[0]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[0] = rate
            if rental_rates_min[0] == []:
                rental_rates_min[0] = '0'

        # renovated bachelor unit
        if w[0] == 'Bachelor' and w[1] == 'Renovated':
            suite_data_list[1] = w

            # determine the vacancy of the renovated bachelor suites
            if 'Available' in suite_data_list[1]:
                is_vacant[1] = True
            if 'Waitlist' in suite_data_list[1]:
                is_vacant[1] = False

            # determine the rate of the renovated bachelor suites
            for element in suite_data_list[1]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[1] = rate
            if rental_rates_min[1] == []:
                rental_rates_min[1] = '0'

        # one bedroom
        if w[0] == 'One' and w[1] == 'Bedroom' and w[2] != 'Renovated':
            suite_data_list[2] = w

            # determine if the one bedroom suites have vacancy
            if 'Available' in suite_data_list[2]:
                is_vacant[2] = True
            if 'Waitlist' in suite_data_list[2]:
                is_vacant[2] = False

            # determine the starting rate for the one bedroom suites
            for element in suite_data_list[2]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[2] = rate
            if rental_rates_min[2] == []:
                rental_rates_min[2] = '0'

        if w[0] == 'One' and w[1] == 'Bedroom' and w[2] == 'Renovated':
            suite_data_list[3] = w

            # determine if the renovated one bedroom suites have vacancy
            if 'Available' in suite_data_list[3]:
                is_vacant[3] = True
            if 'Waitlist' in suite_data_list[3]:
                is_vacant[3] = False

            # determine the starting rate for the renovated one bedroom suites
            for element in suite_data_list[3]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[3] = rate
            if rental_rates_min[3] == []:
                rental_rates_min[3] = '0'

        # two bedroom
        if w[0] == 'Two' and w[1] == 'Bedroom' and w[2] != 'Renovated':
            suite_data_list[4] = w

            # determine if the  two bedroom suites have vacancy
            if 'Available' in suite_data_list[4]:
                is_vacant[4] = True
            if 'Waitlist' in suite_data_list[4]:
                is_vacant[4] = False

            # determine the starting rate for the two bedroom suites
            for element in suite_data_list[4]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[4] = rate
            if rental_rates_min[4] == []:
                rental_rates_min[4] = '0'

        # two bedroom renovated
        if w[0] == 'Two' and w[1] == 'Bedroom' and w[2] == 'Renovated':
            suite_data_list[5] = w

            # determine if the renovated two bedroom suites have vacancy
            if 'Available' in suite_data_list[5]:
                is_vacant[5] = True
            if 'Waitlist' in suite_data_list[5]:
                is_vacant[5] = False

            # determine the starting rate for the renovated two bedroom suites
            for element in suite_data_list[5]:
                if element[0] == '$':
                    rate = element[1:]
                    rental_rates_min[5] = rate
            if rental_rates_min[5] == []:
                rental_rates_min[5] = '0'

    return rental_rates_min, is_vacant

if __name__ == '__main__':
    hi_level_place()