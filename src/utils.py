from typing import Any
import psycopg2


def database_exists(database_name: str, params: dict) -> bool:
    """Проверка существует ли база и есть ли в ней данные, если да, возвращаем TRUE"""
    # result = False
    conn = psycopg2.connect(dbname='postgres', **params)
    cur = conn.cursor()

    cur.execute("""SELECT 1 FROM pg_database WHERE datname = %s""", (database_name,))
    result = cur.fetchone() is not None
    # if cur.fetchone():
    #     conn_hh = psycopg2.connect(dbname=database_name, **params)
    #     cur_hh = conn_hh.cursor()
    #     cur_hh.execute(f"SELECT * FROM vacancies LIMIT 1")
    #     result = cur_hh.fetchone() is not None
    #     cur_hh.close()
    #     conn_hh.close()

    cur.close()
    conn.close()

    return result


def create_database(database_name: str, params: dict, database_is_exists = False):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

    if not database_is_exists:
        conn = psycopg2.connect(dbname='postgres', **params)

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    id_emp SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    open_vacancies INTEGER,
                    employer_url TEXT
                    )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id_vac SERIAL PRIMARY KEY,
                    id_emp INT REFERENCES employers(id_emp),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary REAL,
                    vacancy_url TEXT
                )
            """)
    else:
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                       TRUNCATE TABLE vacancies RESTART IDENTITY CASCADE 
                   """)

        with conn.cursor() as cur:
            cur.execute("""
                TRUNCATE TABLE employers RESTART IDENTITY CASCADE 
            """)

    conn.commit()
    conn.close()


def save_employers_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о работодателях в БД."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            # print(employer)
            cur.execute(
                """
                INSERT INTO employers (id_emp, company_name, open_vacancies, employer_url)
                VALUES (%s, %s, %s, %s)
                """,
                (employer['id'], employer['name'], employer['open_vacancies'], employer['url'])
            )

    conn.commit()
    conn.close()


def save_vacancies_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о вакансиях в БД."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute(
                """
                INSERT INTO vacancies (id_emp, vacancy_name, salary, vacancy_url)
                VALUES (%s, %s, %s, %s)
                """,
                (vacancy['id_emp'], vacancy['name'], vacancy['salary'], vacancy['url'])
            )

    conn.commit()
    conn.close()