import os

from src.config import config
from dotenv import load_dotenv


# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной TOKEN из .env-файла
# api_key = os.getenv('API_KEY')

def main():

    params = config()

    # save_data_to_database(data, 'youtube', params)


if __name__ == '__main__':
    main()