
mkdir -p "data/spaceflight_raw_data"
poetry run python -m src.data_collection.fetch_spaceflight_news \
    "data/spaceflight_raw_data" \
    "src/configs/data_collection/spaceflight_news_baseline.yaml"