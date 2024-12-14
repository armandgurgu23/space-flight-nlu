from sys import argv
from unstructured.partition.html import partition_html
from pandas import DataFrame

def read_raw_data_files(input_path:str) -> DataFrame:
    frames = {
        search_term: v 
    }
    return



class Article_Processor(object):
    
    def __init__(self) -> None:
        pass

    def __call__(self) -> None:
        pass


if __name__ == "__main__":
    dataset_path = argv[1]
    read_raw_data_files(dataset_path)
    breakpoint()
