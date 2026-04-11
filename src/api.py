import requests


def get_employers(search_text):
    url = 'https://api.hh.ru/employers'
    params = {
        'text': search_text,
         'host': 'hh.kz',
        #'area': 1,
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


def get_vacancies(search_text, exclude_text):
    url = 'https://api.hh.ru/vacancies'
    params = {
        #'text': search_text,
        #'exclude': exclude_text,
        #'search_field': 'name',
        'area': 160,
        'period': 30,
        #'only_with_salary': True,
        'employer_id':'25880',
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
            'salary': vacancy['salary']['from'] if vacancy['salary']['from'] is not None else 'Not specified',
            'url': vacancy['url']
        }
      else:
        vacancy_data = {
            'name': vacancy['name'],
            'salary': 'Not specified',
            'url': vacancy['url']
        }
        result.append(vacancy_data)

    return result


# search_text = 'Python developer'
# exclude_text = 'Junior Middle Senior'
# vacancies = get_vacancies(search_text, exclude_text)
#
# for vacancy in vacancies:
#     print(vacancy)