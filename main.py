import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page='
json_data = []

def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()


def get_html(host):
    response = requests.get(host, headers=get_headers())
    hh_python = response.text
    soup = BeautifulSoup(hh_python, features='lxml')
    return soup


def get_max_pages():
    buttons = get_html(HOST).find_all('a', attrs={'data-qa': 'pager-page'})
    for button in buttons:
        list_buttons = []
        list_buttons.append(button.text)
    max_page = int(max(list_buttons))
    return max_page


def get_json_data():
    for i in range((get_max_pages()) - 1):
        page_count = 0
        new_host = HOST + str(page_count)
        vacancies = get_html(new_host).find_all('div', class_="serp-item")
        for vacancy in vacancies:
            header = vacancy.find('a', class_="serp-item__title")
            href = header['href']
            header_parsed = header.text
            sallary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if sallary == None:
                sallary_parsed = 'ЗП не указана'
            else:
                sallary_parsed = sallary.text
            company_name = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
            company_name_parsed = company_name.text
            city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
            city_parsed = city.text
            response = requests.get(href, headers=get_headers())
            hh_python = response.text
            soup = BeautifulSoup(hh_python, features='lxml')
            description = soup.find('div', attrs={'data-qa': 'vacancy-description'})
            keywords = ['Flask', 'Django']
            if description!= None:
                for key in keywords:
                    if key in description.text:
                        vac_data = {
                            'vacacy_name': header_parsed,
                            'href': href,
                            'sallary': sallary_parsed,
                            'company_name': company_name_parsed,
                            'city': city_parsed
                            }
                        json_data.append(vac_data)                
        page_count += 1


if __name__ == '__main__':
    get_json_data()
    with open('hh_py.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    