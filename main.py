import pickle
from datetime import datetime, timezone

from src.oto_dom_scraper import OtodomDataScraper
import config as conf


def get_save_path():
    ts = datetime.now(timezone.utc)
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    return f"./data/query_results_{ts_str}.pkl"


if __name__ == "__main__":
    print("Initializing..")
    scraper = OtodomDataScraper(page_limit=25)

    print("Downloading data..")
    query_cfg = conf.get_query_config().to_dict()
    offers_df = scraper.download_data(**query_cfg)

    print("Saving data..")
    path = get_save_path()
    with open(path, "wb") as p:
        pickle.dump(offers_df, p)

    print(f"Saved {len(offers_df)} offers to: {path}")
