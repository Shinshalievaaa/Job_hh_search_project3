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


def display_interactive_menu(DBManager):

    menu_data = {
        1: {"title": "Список всех компаний и количество вакансий у каждой компании", "function": DBManager.get_companies_and_vacancies_count},
        2: {"title": "Список всех вакансий", "function": DBManager.get_all_vacancies},
        3: {"title": "Средняя зарплата по вакансиям", "function": DBManager.get_avg_salary},
        4: {"title": "Список всех вакансий, у которых зарплата выше средней по всем вакансиям", "function": DBManager.get_vacancies_with_higher_salary},
        5: {"title": "Список всех вакансий, в названии которых содержится текст", "function": DBManager.get_vacancies_with_keyword}
    }
    choice = 0

    while True:
        print("\n--- МЕНЮ ---")
        for number, item in menu_data.items():
            print(f"{number}. {item['title']}")

        while True:
            try:
                choice = int(input("Введите номер пункта: "))
                if 1 <= choice <= 5:
                    break
                else:
                    print("Пожалуйста, введите число от 1 до 5.")
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите целое число.")

        if choice == 5:
            search_text = input("Введите текст для поиска по вакансиям:")
            if search_text:
                func_DBManager = menu_data[choice]['function']
                df = func_DBManager(search_text)
                print_console(df, menu_data[choice]['title'])
        else:
            func_DBManager = menu_data[choice]['function']
            df = func_DBManager()
            print_console(df, menu_data[choice]['title'])

        while True:
            repeat = input("Вывести меню повторно? (Да/Нет): ").lower()
            if repeat in ["да", "нет"]:
                break
            else:
                print("Пожалуйста, ответьте 'Да' или 'Нет'.")

        if repeat == "нет":
            print("До свидания!")
            break


def main(DBManager):

    database_is_exists = database_exists(database_name, params)
    if database_is_exists:
        answer = input("Обновить данные в БД? Ответ (Да/Нет):")
        if answer.lower() == 'да':
            print('Идет обновление данных с hh.ru....')
            database_update(database_is_exists)
    else:
        print('Идет обновление данных с hh.ru....')
        database_update()

    display_interactive_menu(DBManager)


if __name__ == '__main__':
    DBManager = DBManager('hh', params)
    main(DBManager)
