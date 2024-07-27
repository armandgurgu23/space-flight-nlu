from sys import argv
import requests
import polars as pl
from unstructured.partition.html import partition_html
import time


def run_sample_request(limit:int, search_term:str):
    endpoint = f'https://api.spaceflightnewsapi.net/v4/articles/?limit={limit}&search={search_term}'
    response = requests.get(url=endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("API IS DOWN!")
        breakpoint()

def get_us_data_from_url(url:str):
    elems = partition_html(url=url)
    return [(str(el), el.to_dict()['type']) for el in elems]

def extract_element_texts_and_types(url:str):
    try:
        return get_us_data_from_url(url)
    except:
        max_retries = 5
        for i in range(max_retries):
            time.sleep(1)
            try:
                return get_us_data_from_url(url)
            except:
                print(f'Retry {i}/{max_retries} failed!')
        return None


if __name__ == "__main__":
    contents = run_sample_request(100, search_term='SpaceX')
    df = pl.DataFrame(contents['results'])
    df = df.with_columns(
        (
            pl.col('url').map_elements(extract_element_texts_and_types).alias('article_elements')
        )
    )

