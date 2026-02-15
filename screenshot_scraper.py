"""
Screenshot Scraper module.
Downloads app screenshots from Google Play and iOS App Store listings
to support visual documentation of the current Maya app flows.
"""

from __future__ import annotations

import json
import logging
import urllib.request
import urllib.error
from pathlib import Path

import config

logger = logging.getLogger(__name__)


def _download_image(url: str, dest: Path) -> bool:
    """Download an image from a URL and save to dest. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(resp.read())
        return True
    except Exception as e:
        logger.warning(f"Failed to download {url}: {e}")
        return False


def scrape_google_play_screenshots() -> list[dict]:
    """Fetch screenshot URLs from Google Play listing and download them."""
    from google_play_scraper import app as gplay_app

    maya_cfg = config.get("scraper", "maya", {})
    app_id = maya_cfg.get("google_play_app_id", "com.paymaya")

    logger.info(f"Fetching Google Play screenshots for {app_id}...")
    try:
        details = gplay_app(app_id, lang="en", country="ph")
    except Exception as e:
        logger.error(f"Google Play app details fetch failed: {e}")
        return []

    screenshot_urls = details.get("screenshots", [])
    if not screenshot_urls:
        logger.warning("No screenshots found in Google Play listing")
        return []

    logger.info(f"Found {len(screenshot_urls)} Google Play screenshots")
    output_dir = config.output_dir() / "screenshots" / "google_play"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, url in enumerate(screenshot_urls):
        filename = f"screenshot_{i + 1:02d}.png"
        dest = output_dir / filename
        if dest.exists():
            logger.debug(f"  Screenshot {filename} already exists, skipping")
            results.append({
                "platform": "google_play",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })
            continue

        success = _download_image(url, dest)
        if success:
            logger.info(f"  Downloaded {filename}")
            results.append({
                "platform": "google_play",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })

    return results


def scrape_ios_screenshots() -> list[dict]:
    """Fetch screenshot URLs from iOS App Store via iTunes Lookup API."""
    maya_cfg = config.get("scraper", "maya", {})
    app_id = maya_cfg.get("ios_app_id", 1488600019)

    logger.info(f"Fetching iOS App Store screenshots for app ID {app_id}...")
    lookup_url = f"https://itunes.apple.com/lookup?id={app_id}&country=ph"

    try:
        req = urllib.request.Request(lookup_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        logger.error(f"iTunes Lookup API failed: {e}")
        return []

    results_list = data.get("results", [])
    if not results_list:
        logger.warning("No results from iTunes Lookup API")
        return []

    app_data = results_list[0]
    screenshot_urls = app_data.get("screenshotUrls", [])
    ipad_urls = app_data.get("ipadScreenshotUrls", [])

    all_urls = screenshot_urls + ipad_urls
    if not all_urls:
        logger.warning("No screenshots found in iOS listing")
        return []

    logger.info(
        f"Found {len(screenshot_urls)} iPhone + {len(ipad_urls)} iPad screenshots"
    )
    output_dir = config.output_dir() / "screenshots" / "ios"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, url in enumerate(screenshot_urls):
        filename = f"iphone_{i + 1:02d}.png"
        dest = output_dir / filename
        if dest.exists():
            results.append({
                "platform": "ios",
                "device": "iphone",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })
            continue

        success = _download_image(url, dest)
        if success:
            logger.info(f"  Downloaded {filename}")
            results.append({
                "platform": "ios",
                "device": "iphone",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })

    for i, url in enumerate(ipad_urls):
        filename = f"ipad_{i + 1:02d}.png"
        dest = output_dir / filename
        if dest.exists():
            results.append({
                "platform": "ios",
                "device": "ipad",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })
            continue

        success = _download_image(url, dest)
        if success:
            logger.info(f"  Downloaded {filename}")
            results.append({
                "platform": "ios",
                "device": "ipad",
                "index": i + 1,
                "url": url,
                "local_path": str(dest),
            })

    return results


def run() -> dict:
    """
    Download screenshots from both stores. Caches to data/screenshots_manifest.json.
    Returns manifest dict with all downloaded screenshot metadata.
    """
    manifest_path = config.output_dir() / "screenshots_manifest.json"

    if manifest_path.exists():
        logger.info(f"Loading cached screenshot manifest from {manifest_path}")
        with open(manifest_path) as f:
            return json.load(f)

    gplay_shots = scrape_google_play_screenshots()
    ios_shots = scrape_ios_screenshots()

    manifest = {
        "google_play": gplay_shots,
        "ios": ios_shots,
        "total_screenshots": len(gplay_shots) + len(ios_shots),
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info(
        f"Saved screenshot manifest to {manifest_path} "
        f"({manifest['total_screenshots']} screenshots)"
    )

    return manifest
