import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def le_jardin():
    '''Follows same general logic to parse information with beautifulsoup
    to scrape the rental rates, unit types and vacancy availability.

    If you are reading/editing this in an IDE;
        1 - right click -> Run Current File in Interactive Window
        2 - paste ->>  d, c, x = le_jardin(); print('Rental rates:', d, x, '\nVacancies:', c)
        3 - run the code to visualize what the dictionary of units and list of
        vacancy bools (is_vacant)'''
    jardin_min_rates = dict()
    jardin_max_rates = dict()
    is_vacant = ['No Info', 'No Info', 'No Info']
    suite_types = ['1 Bedroom', '1 Bedroom Elite', '1 Bedroom Luxury Elite']
    rental_rates_min = []
    rental_rates_max = []
    url = 'https://greatapartments.ca/mha_property/le-jardin/'
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
        # "Check back soon" when no rate posted
        if rate[0] == 'C':
            temp_rate_list.append('$0-$0')

    print(temp_rate_list)

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

    # temporarily reorder these rates according to their order on the website; monitor this
    reordered_min_rates = [rental_rates_min[2], rental_rates_min[1], 
                           rental_rates_min[0]]
    reordered_max_rates = [rental_rates_max[2], rental_rates_max[1],
                           rental_rates_max[0]]

    """Vacancy status is unknown, comment on the availability column
        that only "Book a viewing" is showing per suite type"""

    for unit in suite_types:
        min_ = rental_rates_min.pop(0)
        max_ = rental_rates_max.pop(0)
        jardin_min_rates[unit] = min_
        jardin_max_rates[unit] = max_

    #print(jardin_min_rates, jardin_max_rates, is_vacant)
    return jardin_min_rates, jardin_max_rates, is_vacant

if __name__ == '__main__':
    le_jardin()