
dataset="2024-12-14"
output_path="data/spaceflight_raw_data/${dataset}"

mkdir -p $output_path

poetry run python -m src.data_collection.fetch_spaceflight_news \
    $output_path \
    "src/configs/data_collection/spaceflight_news_baseline.yaml"

# poetry run python -m src.data_processing.get_full_article_text \
#     "data/spaceflight_raw_data/${dataset}"