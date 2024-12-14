
dataset="2024-08-05"
mkdir -p "data/spaceflight_raw_data"
poetry run python -m src.data_collection.fetch_spaceflight_news \
    "data/spaceflight_raw_data" \
    "src/configs/data_collection/spaceflight_news_baseline.yaml"

poetry run python -m src.data_processing.get_full_article_text \
    "data/spaceflight_raw_data/${dataset}"