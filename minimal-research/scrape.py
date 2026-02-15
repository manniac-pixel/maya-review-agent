"""
Scrape Maya and GCash reviews from Google Play + iOS App Store.
Last 6 months only. Targets ~2000-3000 reviews total.
Saves to data/reviews.csv
"""

import time
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews as gplay_reviews
from app_store_scraper import AppStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"
OUTPUT = DATA_DIR / "reviews.csv"
MONTHS = 6
CUTOFF = datetime.now() - timedelta(days=MONTHS * 30)

APPS = {
    "maya": {
        "gplay_id": "com.paymaya",
        "ios_name": "maya-savings-credit-crypto",
        "ios_id": 1488600019,
    },
    "gcash": {
        "gplay_id": "com.globe.gcash.android",
        "ios_name": "gcash",
        "ios_id": 520020791,
    },
}


def scrape_gplay(app_id: str, app_label: str) -> list[dict]:
    """Scrape Google Play reviews, newest first, stop at cutoff."""
    log.info(f"[{app_label}] Scraping Google Play ({app_id})...")
    all_reviews = []
    token = None

    for batch in range(1, 30):  # max 30 batches × 200 = 6000 ceiling
        try:
            result, token = gplay_reviews(
                app_id, lang="en", country="ph",
                sort=Sort.NEWEST, count=200,
                continuation_token=token,
            )
        except Exception as e:
            log.warning(f"[{app_label}] GP batch {batch} error: {e}")
            time.sleep(3)
            continue

        if not result:
            break

        hit_cutoff = False
        for r in result:
            dt = r.get("at")
            if dt and dt < CUTOFF:
                hit_cutoff = True
                break
            text = (r.get("content") or "").strip()
            if text:
                all_reviews.append({
                    "app": app_label,
                    "platform": "Android",
                    "date": dt,
                    "rating": r.get("score"),
                    "text": text,
                })

        log.info(f"  batch {batch}: +{len(result)} (total: {len(all_reviews)})")
        if hit_cutoff or token is None:
            break
        time.sleep(random.uniform(1, 2))

    return all_reviews


def scrape_ios(app_name: str, app_id: int, app_label: str) -> list[dict]:
    """Scrape iOS App Store reviews."""
    log.info(f"[{app_label}] Scraping iOS App Store ({app_name})...")
    try:
        app = AppStore(country="ph", app_name=app_name, app_id=app_id)
        app.review(how_many=3000)
    except Exception as e:
        log.error(f"[{app_label}] iOS scrape failed: {e}")
        return []

    reviews = []
    for r in app.reviews:
        dt = r.get("date")
        if hasattr(dt, "replace"):
            dt = dt.replace(tzinfo=None)
        if dt and dt < CUTOFF:
            continue
        text = (r.get("review") or "").strip()
        if text:
            reviews.append({
                "app": app_label,
                "platform": "iOS",
                "date": dt,
                "rating": r.get("rating"),
                "text": text,
            })

    log.info(f"[{app_label}] iOS: {len(reviews)} reviews")
    return reviews


def run():
    if OUTPUT.exists():
        df = pd.read_csv(OUTPUT)
        log.info(f"Already have {len(df)} reviews in {OUTPUT}. Delete to re-scrape.")
        return df

    all_reviews = []
    for label, cfg in APPS.items():
        all_reviews.extend(scrape_gplay(cfg["gplay_id"], label))
        all_reviews.extend(scrape_ios(cfg["ios_name"], cfg["ios_id"], label))

    df = pd.DataFrame(all_reviews)
    df = df.sort_values("date", ascending=False).reset_index(drop=True)

    # Sample down if we got too many (target ~3000)
    if len(df) > 3000:
        log.info(f"Got {len(df)} reviews, sampling down to 3000...")
        df = df.sample(n=3000, random_state=42).reset_index(drop=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    log.info(f"Saved {len(df)} reviews to {OUTPUT}")

    # Quick stats
    for app in df["app"].unique():
        sub = df[df["app"] == app]
        log.info(f"  {app}: {len(sub)} reviews, avg rating {sub['rating'].mean():.1f}")

    return df


if __name__ == "__main__":
    run()
