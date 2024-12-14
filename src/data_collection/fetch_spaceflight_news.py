from unstructured.partition.html import partition_html
import requests
import os
from sys import argv
from omegaconf import OmegaConf
from tqdm import tqdm
from datetime import datetime
from pandas import DataFrame, concat

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
                curr_df = self.extract_news_across_multiple_pages(curr_response)
            else:
                curr_df = DataFrame(curr_response['results'])
            # Now write the results to file.
            if curr_df.shape[0] > 0:
                print(f'{curr_term} returned {curr_df.shape[0]} results!')
                curr_df.to_parquet(
                    os.path.join(term_output_path, 'response_results.parquet')
                )
            else:
                print(f'WARNING: No results returned for search term {curr_term}')
    
    def extract_news_across_multiple_pages(self, response:dict[str]):
        expected_results = response['count']
        output_frames = []
        while response['next'] and response['results']:
            output_frames.append(DataFrame(response['results']))
            response = self.send_request_to_api(response['next'])
        # After the loop breaks, add the last page of results.
        output_frames.append(DataFrame(response['results']))
        output_frames = concat(output_frames)
        print(f'Finished querying with pagination. Collected results: {output_frames.shape}; Expected results: {expected_results}')
        return output_frames
    
    def send_request_to_api(self, endpoint:str):
        response = requests.get(url=endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("API IS DOWN!")
            breakpoint()

    def query_spaceflight_api(self, limit:int, search_term:str):
        endpoint = f'https://api.spaceflightnewsapi.net/v4/articles/?limit={limit}&search={search_term}'
        return self.send_request_to_api(endpoint)
    
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

    

