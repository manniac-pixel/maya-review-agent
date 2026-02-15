"""
Scraper module for app reviews from Google Play Store and iOS App Store.
Collects reviews from the last N months, extracts structured data, and saves to CSV.
Supports Maya (default) and GCash.
"""

from __future__ import annotations

import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews as gplay_reviews
from app_store_scraper import AppStore

import config

logger = logging.getLogger(__name__)


def scrape_google_play(
    months: int,
    app_id: str | None = None,
    label: str = "Google Play",
) -> pd.DataFrame:
    """Scrape reviews from Google Play Store for a given app."""
    if app_id is None:
        app_id = config.get("scraper", "maya", {}).get(
            "google_play_app_id", "com.paymaya"
        )
    batch_size = config.get("scraper", "gplay_batch_size", 200)
    max_batches = config.get("scraper", "gplay_max_batches", 50)
    sleep_seconds = config.get("scraper", "gplay_sleep_seconds", 1.5)

    logger.info(f"Scraping {label} reviews (app: {app_id})...")
    cutoff = datetime.now() - timedelta(days=months * 30)
    all_reviews = []
    continuation_token = None

    for batch_num in range(1, max_batches + 1):
        try:
            result, continuation_token = gplay_reviews(
                app_id,
                lang="en",
                country="ph",
                sort=Sort.NEWEST,
                count=batch_size,
                continuation_token=continuation_token,
            )
        except Exception as e:
            logger.warning(f"{label} batch {batch_num} failed: {e}")
            time.sleep(3)
            continue

        if not result:
            logger.info(f"No more {label} reviews after batch {batch_num}")
            break

        batch_reviews = []
        past_cutoff = False
        for r in result:
            review_date = r.get("at")
            if review_date and review_date < cutoff:
                past_cutoff = True
                break
            batch_reviews.append({
                "date": review_date,
                "rating": r.get("score"),
                "text": r.get("content", ""),
                "app_version": r.get("reviewCreatedVersion", ""),
                "platform": "Android",
            })

        all_reviews.extend(batch_reviews)
        logger.info(
            f"  {label} batch {batch_num}: {len(batch_reviews)} reviews "
            f"(total: {len(all_reviews)})"
        )

        if past_cutoff or continuation_token is None:
            break

        time.sleep(sleep_seconds)

    df = pd.DataFrame(all_reviews)
    logger.info(f"{label}: collected {len(df)} reviews")
    return df


def scrape_ios_app_store(
    months: int,
    app_name: str | None = None,
    app_id: int | None = None,
    label: str = "iOS App Store",
) -> pd.DataFrame:
    """Scrape reviews from iOS App Store for a given app."""
    maya_cfg = config.get("scraper", "maya", {})
    if app_name is None:
        app_name = maya_cfg.get("ios_app_name", "maya-savings-credit-crypto")
    if app_id is None:
        app_id = maya_cfg.get("ios_app_id", 1488600019)
    ios_review_count = config.get("scraper", "ios_review_count", 5000)
    fallback_countries = config.get("scraper", "ios_fallback_countries", ["us", "gb"])
    sleep_seconds = config.get("scraper", "ios_sleep_seconds", 2)

    logger.info(f"Scraping {label} reviews (app: {app_name})...")
    cutoff = datetime.now() - timedelta(days=months * 30)

    countries_to_try = ["ph"] + [c for c in fallback_countries if c != "ph"]
    app_reviews = []

    for country in countries_to_try:
        try:
            logger.info(f"  {label}: trying country={country}...")
            app = AppStore(country=country, app_name=app_name, app_id=app_id)
            app.review(how_many=ios_review_count)
            logger.info(
                f"  {label} country={country}: app.review() returned "
                f"{len(app.reviews)} reviews"
            )
            if app.reviews:
                app_reviews = app.reviews
                break
            else:
                logger.warning(
                    f"  {label} country={country}: 0 reviews returned (silent failure). "
                    "Trying next country..."
                )
        except Exception as e:
            logger.warning(f"  {label} country={country} failed: {e}")
        time.sleep(sleep_seconds)

    if not app_reviews:
        logger.error(
            f"{label}: no reviews from any country ({countries_to_try}). "
            "iOS scraper may be rate-limited or the app listing has changed."
        )
        return pd.DataFrame()

    all_reviews = []
    for r in app_reviews:
        review_date = r.get("date")
        if hasattr(review_date, "replace"):
            review_date = review_date.replace(tzinfo=None)
        if review_date and review_date < cutoff:
            continue
        all_reviews.append({
            "date": review_date,
            "rating": r.get("rating"),
            "text": r.get("review", ""),
            "app_version": r.get("version", ""),
            "platform": "iOS",
        })

    df = pd.DataFrame(all_reviews)
    logger.info(f"{label}: collected {len(df)} reviews")
    return df


def _combine_and_clean(dfs: list[pd.DataFrame], output_path: Path) -> pd.DataFrame:
    """Concatenate DataFrames, drop empty text, sort by date, and save."""
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.dropna(subset=["text"])
    combined = combined[combined["text"].str.strip().astype(bool)]
    combined = combined.sort_values("date", ascending=False).reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False)
    logger.info(f"Saved {len(combined)} reviews to {output_path}")
    return combined


def run(months: int = 12) -> pd.DataFrame:
    """
    Scrape Maya reviews from both stores. If raw_reviews.csv already exists and
    has data, skip scraping and return cached data (resume support).
    """
    output_path = config.output_dir() / "raw_reviews.csv"
    if output_path.exists():
        existing = pd.read_csv(output_path, parse_dates=["date"])
        if len(existing) > 0:
            logger.info(
                f"Found existing {output_path} with {len(existing)} reviews. "
                "Skipping scrape. Delete the file to re-scrape."
            )
            return existing

    gplay_df = scrape_google_play(months)
    ios_df = scrape_ios_app_store(months)
    return _combine_and_clean([gplay_df, ios_df], output_path)


def run_gcash(months: int = 12) -> pd.DataFrame:
    """
    Scrape GCash reviews from both stores. If gcash_reviews.csv already exists
    and has data, skip scraping and return cached data.
    """
    gcash_output_path = config.output_dir() / "gcash_reviews.csv"
    gcash_cfg = config.get("scraper", "gcash", {})

    if gcash_output_path.exists():
        existing = pd.read_csv(gcash_output_path, parse_dates=["date"])
        if len(existing) > 0:
            logger.info(
                f"Found existing {gcash_output_path} with {len(existing)} reviews. "
                "Skipping GCash scrape. Delete the file to re-scrape."
            )
            return existing

    gplay_path = config.output_dir() / "gcash_gplay_temp.csv"
    try:
        gplay_df = scrape_google_play(
            months,
            app_id=gcash_cfg.get("google_play_app_id", "com.globe.gcash.android"),
            label="GCash Google Play",
        )
        gplay_df.to_csv(gplay_path, index=False)
        logger.info(f"Saved intermediate GCash Google Play reviews to {gplay_path}")
    except Exception as e:
        logger.error(f"Failed to scrape GCash Google Play: {e}")
        gplay_df = pd.DataFrame()

    ios_path = config.output_dir() / "gcash_ios_temp.csv"
    try:
        ios_df = scrape_ios_app_store(
            months,
            app_name=gcash_cfg.get("ios_app_name", "gcash"),
            app_id=gcash_cfg.get("ios_app_id", 520020791),
            label="GCash iOS App Store",
        )
        ios_df.to_csv(ios_path, index=False)
        logger.info(f"Saved intermediate GCash iOS reviews to {ios_path}")
    except Exception as e:
        logger.error(f"Failed to scrape GCash iOS: {e}")
        ios_df = pd.DataFrame()

    combined = _combine_and_clean([gplay_df, ios_df], gcash_output_path)
    
    # Cleanup temp files
    if gplay_path.exists(): gplay_path.unlink()
    if ios_path.exists(): ios_path.unlink()
    
    return combined
