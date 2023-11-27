import requests
import pandas as pd
from sqlalchemy import create_engine

def get_data_from_api():
    api_url = "http://103.150.197.96:5005/api/v1/rekapitulasi_v2/jabar/harian"
    api_params = {"level": "kab"}

    response = requests.get(api_url, params=api_params, headers={"accept": "application/json"})

    if response.status_code == 200:
        api_data = response.json()['data']['content']

        df = pd.DataFrame(api_data)

        engine = create_engine(f'mysql+mysqlconnector://mysql:mysql@192.168.100.11:3307/mysql')

        df.to_sql('covid_jabar', con=engine, if_exists='replace', index=False)
    else:
        raise ValueError(f"API request failed with status code: {response.status_code}")

if __name__ == "__main__":
    get_data_from_api()