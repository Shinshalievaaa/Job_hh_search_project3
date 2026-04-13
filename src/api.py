import requests


def get_employers(search_text):
    url = 'https://api.hh.ru/employers'
    params = {
        'text': search_text,
        'host': 'hh.kz',
        'only_with_vacancies': True,
        'per_page': 100,
        'page': 0
    }

    employers = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        employers += data['items']

        if data['pages'] == params['page']:
            break
        else:
            params['page'] += 1

    result = []
    for employer in employers:
        employer_data = {
            'id': employer['id'],
            'name': employer['name'],
            'open_vacancies': employer['open_vacancies'],
            'url': employer['url'],
            'vacancies_url': employer['vacancies_url']
        }
        result.append(employer_data)

    return result


def get_vacancies(list_emp):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'area': 160,
        'period': 30,
        'employer_id':list_emp,
        'per_page': 100,
        'page': 0
    }

    vacancies = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        vacancies += data['items']

        if data['pages'] == params['page']:
            break
        else:
            params['page'] += 1

    result = []
    for vacancy in vacancies:
        if vacancy['salary'] is not None:
            vacancy_data = {
                'name': vacancy['name'],
                'salary': vacancy['salary']['from'],# if vacancy['salary']['from'] is not None else 'Not specified',
                'url': vacancy['url'],
                'id_emp': vacancy['employer']['id']
            }
        else:
            vacancy_data = {
                'name': vacancy['name'],
                'salary': None,
                'url': vacancy['url'],
                'id_emp': vacancy['employer']['id']
            }
        result.append(vacancy_data)

    return result


# search_text = 'Python developer'
# exclude_text = 'Junior Middle Senior'
# vacancies = get_vacancies(search_text, exclude_text)
#
# for vacancy in vacancies:
#     print(vacancy)


# search_text_list = ['Kaspi.kz', 'Freedom Holding', 'BI Group']
# employers = []
# for search_text in search_text_list:
#     employers += get_employers(search_text)
#     # employers_list.append(employers)
#
# for employer in employers:
#   print(employer)