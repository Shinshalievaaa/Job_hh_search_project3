import pandas as pd
import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT company_name as company_name, SUM(open_vacancies) as open_vacancies FROM employers GROUP BY id_emp"""
            )
            df = pd.DataFrame(
                cur.fetchall(),
                columns=[description[0] for description in cur.description],
            )
            df = df.rename(
                columns={
                    "company_name": "Имя компании",
                    "open_vacancies": "Количество вакансий",
                }
            )
            cur.close()

        return df

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT vacancy_name, company_name, COALESCE(salary,0) as salary, vacancy_url
                        FROM vacancies INNER JOIN employers ON vacancies.id_emp = employers.id_emp 
                        """
            )
            df = pd.DataFrame(
                cur.fetchall(),
                columns=[description[0] for description in cur.description],
            )
            df = df.rename(
                columns={
                    "vacancy_name": "Вакансия",
                    "company_name": "Имя компании",
                    "salary": "Зарплата",
                    "vacancy_url": "Ссылка на вакансию",
                }
            )
            cur.close()

        return df

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT vacancy_name, AVG(COALESCE(salary,0)) AS salary
                            FROM vacancies WHERE salary > 0 GROUP BY vacancy_name 
                               """)
            df = pd.DataFrame(
                cur.fetchall(),
                columns=[description[0] for description in cur.description],
            )
            df = df.rename(columns={"vacancy_name": "Вакансия", "salary": "Зарплата"})
            cur.close()

        return df

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT vacancy_name, AVG(COALESCE(salary,0)) AS salary
                            FROM vacancies 
                            GROUP BY vacancy_name
                            HAVING AVG(COALESCE(salary,0)) > (SELECT AVG(COALESCE(salary,0)) FROM vacancies)
                            ORDER BY salary DESC
                        """)
            df = pd.DataFrame(
                cur.fetchall(),
                columns=[description[0] for description in cur.description],
            )
            df = df.rename(columns={"vacancy_name": "Вакансия", "salary": "Зарплата"})
            cur.close()

        return df

    def get_vacancies_with_keyword(self, search_text):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT DISTINCT vacancy_name FROM vacancies 
                            WHERE LOWER(vacancy_name) LIKE LOWER(%s)
                        """,
                ("%" + search_text + "%",),
            )
            df = pd.DataFrame(
                cur.fetchall(),
                columns=[description[0] for description in cur.description],
            )
            df = df.rename(columns={"vacancy_name": "Вакансия"})
            cur.close()

        return df
