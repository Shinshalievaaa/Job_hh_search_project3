import os

from src.utils import create_database, save_employers_to_database, save_employers_to_database, \
    save_vacancies_to_database, database_exists
from src.api import get_vacancies, get_employers
from src.db_manager import DBManager
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table


# Загрузка переменных из .env-файла
load_dotenv()

params = {}
params['host'] = os.getenv('host')
params['user'] = os.getenv('user')
params['password'] = os.getenv('password')
params['port'] = os.getenv('port')
database_name = os.getenv('dbname')

search_text_list = ['Kaspi.kz', 'Freedom Holding', 'BI Group']

def database_update(database_is_exists = False):
    """Создание БД, получение данных по API и сохранение их в БД"""
    create_database(database_name, params, database_is_exists)

    data_employers = []
    for search_text in search_text_list:
        data_employers += get_employers(search_text)

    list_emp = []
    for employer in data_employers:
        list_emp.append(employer['id'])

    data_vacancies = get_vacancies(list_emp)

    # create_database('hh', params)

    save_employers_to_database(data_employers, 'hh', params)

    save_vacancies_to_database(data_vacancies, 'hh', params)


def print_console(df, title):
    """Вывод полученных данных по запросу в консоль"""
    console = Console()

    table = Table(title=title)

    for col in df.columns:
        if col == 'Зарплата':
            table.add_column(col, style="magenta", no_wrap=True, width=20)
        else:
            table.add_column(col, style="cyan", no_wrap=True)

    for _, row in df.iterrows():
        table.add_row(*[str(item) for item in row.values])

    console.print(table)


def main(DBManager):

    database_is_exists = database_exists(database_name, params)
    if database_is_exists:
        answer = input("Обновить данные в БД? Ответ (y/n):")
        if answer.lower() == 'y':
            print('Идет обновление данных с hh.ru....')
            database_update(database_is_exists)
    else:
        print('Идет обновление данных с hh.ru....')
        database_update()

    df_employers = DBManager.get_companies_and_vacancies_count()
    title = "Список всех компаний и количество вакансий у каждой компании"
    print_console(df_employers, title)

    df_all_vacancies = DBManager.get_all_vacancies()
    title = "Список всех вакансий"
    print_console(df_all_vacancies, title)

    df_vacancies_avg_salary = DBManager.get_avg_salary()
    title = "Средняя зарплата по вакансиям"
    print_console(df_vacancies_avg_salary, title)

    df_vacancies_higher_salary = DBManager.get_vacancies_with_higher_salary()
    title = "Список всех вакансий, у которых зарплата выше средней по всем вакансиям"
    print_console(df_vacancies_higher_salary, title)

    search_text = input("Введите текст для поиска по вакансиям:")
    if search_text:
        df_vacancies_list = DBManager.get_vacancies_with_keyword(search_text)
        title = f'Список всех вакансий, в названии которых содержится текст: {search_text}'
        print_console(df_vacancies_list, title)
    else:
        print("Не был введен текст для поиска")


if __name__ == '__main__':
    DBManager = DBManager('hh', params)
    main(DBManager)
