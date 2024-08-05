from unstructured.partition.html import partition_html
import requests
import os
from sys import argv
from omegaconf import OmegaConf
from tqdm import tqdm
from datetime import datetime
from pandas import DataFrame

def get_timestamp(date_only:bool = True):
    return datetime.now().strftime("%Y-%m-%d") if date_only else datetime.now().strftime("%Y-%m-%d_%H:%M:%S") 

class Space_Flight_API_Fetcher(object):
    def __init__(self, output_path:str) -> None:
        self.output_path = output_path
        self.create_output_dir(output_path)
    
    def __call__(self, num_results:int, search_terms:list[str]):

        current_date = get_timestamp()

        for curr_term in tqdm(search_terms, desc=f'Fetching {num_results} articles for each search term'):
            term_output_path = os.path.join(self.output_path, current_date, curr_term)
            os.makedirs(
                term_output_path,
                exist_ok=True
            )
            curr_response = self.query_spaceflight_api(limit=num_results, search_term=curr_term)
            if curr_response['count'] > num_results:
                self.extract_news_across_multiple_pages(curr_response)
            else:
                curr_df = DataFrame(curr_response['results'])
                if curr_df.shape[0] > 0:
                    print(f'{curr_term} returned {curr_df.shape[0]} results!')
                    curr_df.to_parquet(
                        os.path.join(term_output_path, 'response_results.parquet')
                    )
                else:
                    print(f'WARNING: No results returned for search term {curr_term}')
    
    def extract_news_across_multiple_pages(self, response:dict[str]):
        raise NotImplementedError('Add support for handling paginated results!')

    def query_spaceflight_api(self, limit:int, search_term:str):
        endpoint = f'https://api.spaceflightnewsapi.net/v4/articles/?limit={limit}&search={search_term}'
        response = requests.get(url=endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("API IS DOWN!")
            breakpoint()
    
    def create_output_dir(self, output_path:str):
        os.makedirs(output_path, exist_ok=True)
        return

if __name__ == "__main__":
    output_root = argv[1]
    config = OmegaConf.load(argv[2])
    sp_news_fetcher = Space_Flight_API_Fetcher(
        output_path=output_root
    )
    sp_news_fetcher(
        num_results=config.results_per_search,
        search_terms=config.search_terms
    )

    

