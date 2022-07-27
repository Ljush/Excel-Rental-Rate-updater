import requests
from bs4 import BeautifulSoup
'''BeautifulSoup documentation
https://beautiful-soup-4.readthedocs.io/en/latest/

Python requests module documentation
https://www.w3schools.com/python/module_requests.asp'''
def miller_ridge():
    """As of June 13th 2022, no suite cards are posted, only stating
    that 'Spacious apartments in edmonton' starting at $1080/month"""
    url = 'https://www.millerridge.ca/'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}
    page = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(page.content, 'html.parser')
    suite_types = ['One Bedroom', 'One Bedroom+', 'Two Bedroom', 'Two Bedroom+']
    miller_min = dict()
    one_beds = ['One Bedroom', 'One Bedroom+']
    two_beds = ['Two Bedroom', 'Two Bedroom+']
    suite_list = []
    is_vacant = [False, False, False, False]

    # grab one/two bedroom cards from website
    section = page_parsed.findAll('div', 'content')
    for i in section:
        curr = i.text
        curr = curr.replace('\n', ' ')
        curr = curr.strip()
        curr = curr.split()
        suite_list.append(curr)

    # extract both "from $xx-$xx" values
    one_bed_rents = []
    two_bed_rents = []
    for j in suite_list:
        if j[0] == 'One':
            for k in j:
                if k[0] == '$':
                    one_bed_rents.append(k.replace('$', ''))
        if j[0] == 'Two':
            for k in j:
                if k[0] == '$':
                    two_bed_rents.append(k.replace('$', ''))

    single_dic = {}
    double_dic = {}
    for x in one_beds:
        if len(one_bed_rents) >= 1:
            rate = one_bed_rents.pop(0)
            single_dic[x] = rate
        else:
            single_dic[x] = '0'

    for y in two_beds:
        if len(two_bed_rents) >= 1:
            rate_ = two_bed_rents.pop(0)
            double_dic[y] = rate_
        else:
            double_dic[y] = '0'

    #print(single_dic, double_dic)

    for index, z in enumerate(suite_types):
        if index < 2:
            miller_min[z] = single_dic[z]
            if single_dic[z] != '0':
                is_vacant[index] = True
        if index >= 2:
            miller_min[z] = double_dic[z]
            if double_dic[z] != '0':
                is_vacant[index] = True

    #print(miller_min, is_vacant)
    return miller_min, is_vacant

if __name__ == '__main__':
    miller_ridge()