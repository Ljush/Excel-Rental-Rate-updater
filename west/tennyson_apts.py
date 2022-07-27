import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def tennyson_apts():
    tennyson_suite_min = dict()
    tennyson_suite_max = dict()
    suite_types = ['645 sqft', '892 sqft']
    is_vacant = [False, False]
    url = 'https://www.realstar.ca/apartments/ab/edmonton/tennyson-apartments/floorplans.aspx'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    
    """excel sheet on west sheet only accounts for 2 types of units, 
    645 sqft (1 br 1 bath) (variation A), 892 sqft (2br 2 bath) (variation C)"""
    # grab (#text <- .next_sibling of span sr-only class) for rents
    page_info = page_parsed.findAll('span', 'sr-only')
    span_class_text = []
    # reorganize the span 'sr-only' classes into a list
    for j in page_info:
        if j.next_sibling is None:
            continue
        ele = j.next_sibling.text.strip()
        span_class_text.append(ele)
    # extract rental rates per variation per suite type>(1 bed, 2 bed)
    suite_list, one_bed_data, two_bed_data = extract_rates(span_class_text)
    current_excel_list = [one_bed_data['1b A'], two_bed_data['2b C']]
    #print(current_excel_list)

    if len(current_excel_list[0]) != 2 and len(current_excel_list[0]) != 0:
        current_excel_list[0].append('0')
    if len(current_excel_list[1]) != 2 and len(current_excel_list[1]) != 0:
        current_excel_list[1].append('0')
    """just using var a and var c since excel sheet only looks for two rental rates currently
    ; to-do, account for all 6 suite_types/variations"""
    for unit in suite_types:
        rate_list = current_excel_list.pop(0)
        min_rate = rate_list[0]
        max_rate = rate_list[1]
        tennyson_suite_min[unit] = min_rate
        tennyson_suite_max[unit] = max_rate

    #print(tennyson_suite_min, tennyson_suite_max, is_vacant)
    return tennyson_suite_min, tennyson_suite_max, is_vacant

def str_clean(string):
    temp = string
    temp = temp.replace('$', '')
    temp = temp.replace('-', '')
    temp = temp.replace(',', '')
    temp = temp.strip()
    return temp


def extract_rates(span_class_text):
    """extract rental rates per type of suite + variation of suite type"""
    suite_list = [[], [], [], [], [], []]
    variation_data = {}
    variation = {'A': 1, 'B': 2, 'C': 3}
    rate_min_str = ''
    rate_max_str = ''
    # Variation A/B/C can exist in either 1 bed or 2 bed options
    bedroom_state = 1
    for index, i in enumerate(span_class_text):
        element = i

        # current<< flag for current variation currently on rotation in for loop
        if element[0:5] == 'Varia':
            current = element
            continue
        # 1 bed
        if element == '1 / 1':
            bedroom_state = 1
            continue
        # 2 bed
        if element == '2 / 2':
            bedroom_state = 2
            continue

        if element[0] == '$' and rate_min_str == '':
            rate_min_str = str_clean(element)

        # determines if min and max rate are offered; default max is 0 otherwise
        if element[-1] == '-':
            rate_min_str = str_clean(element)
            rate_max_str = str_clean(span_class_text[index+1])
            continue

        if rate_min_str != '':
            suite_index = variation[current[-1]]
            if bedroom_state == 1:
                suite_list[suite_index-1].append(rate_min_str)
                rate_min_str = ''
            if bedroom_state == 2:
                suite_list[suite_index+2].append(rate_min_str)
                rate_min_str = ''

        if rate_max_str != '':
            suite_index = variation[current[-1]]
            if bedroom_state == 1:
                suite_list[suite_index-1].append(rate_max_str)
                rate_max_str = ''
                continue
            if bedroom_state == 2:
                suite_list[suite_index+2].append(rate_max_str)
                rate_max_str = ''
                continue
    
    one_bed_data = {"1b A": suite_list[0], "1b B": 
        suite_list[1], "1b C": suite_list[2]}
    two_bed_data = {"2b A": suite_list[3], "2b B": suite_list[4], "2b C":
                suite_list[5]}

    return suite_list, one_bed_data, two_bed_data
    
if __name__ == '__main__':
    tennyson_apts()