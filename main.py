import requests
import unicodedata
import bs4
from fake_headers import Headers
import json
from pprint import pprint


def get_fake_headers():
    return Headers(browser='chrome', os='win').generate()


def get_vacancies():
    vacancies = []
    vacancies_usd = []
    keywords = 'python, django, flask'

    for ind in range(0, 10):
        url = f'https://spb.hh.ru/search/vacancy?text={keywords}&area=1&area=2&page={ind}'
        response = requests.get(url, headers=get_fake_headers())

        main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
        vacancies_tags = main_page_data.findAll('div', class_='vacancy-serp-item-body__main-info')
        for vacancies_tag in vacancies_tags:
            h3_tag = vacancies_tag.find('h3', class_='bloko-header-section-3')
            salary_tag = vacancies_tag.find('span', class_='bloko-header-section-2')

            if salary_tag is not None:
                salary = salary_tag.text.strip()
                salary = unicodedata.normalize('NFKD', salary)

                info_tag = vacancies_tag.find('div', class_='vacancy-serp-item__info')
                inf_result = info_tag.find_all('div', class_='bloko-text')
                company_name = inf_result[0].text.strip()
                company_name = unicodedata.normalize('NFKD', company_name)
                city = inf_result[1].text.strip().replace('\xa0', ' ')
                a_tag = h3_tag.find('a', class_='bloko-link')
                link = a_tag['href']
                title = a_tag.find('span').text.strip()
                if '$' in salary:
                    vacancies_usd.append({
                        'company_name': company_name,
                        'city': city,
                        'title': title,
                        'salary': salary,
                        'link': link
                    })
                else:
                    vacancies.append({
                        'company_name': company_name,
                        'city': city,
                        'title': title,
                        'salary': salary,
                        'link': link
                    })

    return vacancies, vacancies_usd


if __name__ == '__main__':
    vacancies, vacancies_usd = get_vacancies()

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(vacancies, ensure_ascii=False, indent=4))
    with open('vacancies_usd.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(vacancies_usd, ensure_ascii=False, indent=4))
    pprint(vacancies)
    pprint(vacancies_usd)
