from sys import argv
import requests
import polars as pl
from unstructured.partition.html import partition_html


def run_sample_request(limit:int, search_term:str):
    endpoint = f'https://api.spaceflightnewsapi.net/v4/articles/?limit={limit}&search={search_term}'
    response = requests.get(url=endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("API IS DOWN!")
        breakpoint()

def extract_element_texts_and_types(url:str):
    elems = partition_html(url=url)
    return [(str(el), el.to_dict()['type']) for el in elems]



if __name__ == "__main__":
    contents = run_sample_request(500, search_term='SpaceX')
    df = pl.DataFrame(contents['results'])
    df.select(pl.col('url').map_elements(extract_element_texts_and_types, return_dtype=pl.String)).alias('article_elements')

    # partition_html(url=)
    breakpoint()

