#!/usr/bin/env python3
"""
Maya Review Analysis Agent
==========================
Scrapes Maya fintech app reviews from Google Play and iOS App Store,
performs temporal and comprehensive analysis using Gemini API,
and generates a ranked UX insights report.

Usage:
    python main.py --months 12
    python main.py --months 6 --skip-scrape
    python main.py --stars 1              # Analyze only 1-star reviews
    python main.py --stars 1,2            # Analyze 1 and 2-star reviews
    python main.py --backend ollama --skip-scrape   # Use local Ollama (free, no API key)
    python main.py --backend gemini --skip-scrape   # Use Gemini cloud API
    python main.py --fresh                # Delete cached data and re-run everything
    python main.py --verbose              # Show DEBUG-level logs
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table

import config
import llm
import scraper
import data_quality
import temporal_analyzer
import comprehensive_analyzer
import competitor_analysis
import funnel_analyzer
import accessibility_analyzer
import screenshot_scraper
import insights_generator

load_dotenv()

console = Console()


def setup_logging(verbose: bool = False):
    """Configure logging with Rich console handler and optional file handler."""
    level = logging.DEBUG if verbose else logging.INFO

    # Rich console handler
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True,
    )
    rich_handler.setLevel(level)

    # File handler
    log_file = config.get("logging", "file", "data/maya_agent.log")
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S")
    )

    logging.basicConfig(
        level=level,
        handlers=[rich_handler, file_handler],
    )


def output_suffix(stars: list[int] | None) -> str:
    """Return a file suffix like '_1star' or '_1_2star' for filtered runs."""
    if not stars:
        return ""
    return "_" + "_".join(str(s) for s in sorted(stars)) + "star"


def all_output_paths(suffix: str) -> list[Path]:
    """Return all output file paths for a given suffix."""
    d = config.output_dir()
    return [
        d / "raw_reviews.csv",
        d / "gcash_reviews.csv",
        d / f"temporal_analysis{suffix}.json",
        d / f"comprehensive_analysis{suffix}.json",
        d / f"funnel_analysis{suffix}.json",
        d / f"accessibility_analysis{suffix}.json",
        d / f"competitor_comparison{suffix}.json",
        d / f"journey_map{suffix}.json",
        d / f"final_insights{suffix}.json",
        d / f"maya_insights_report{suffix}.md",
        d / "screenshots_manifest.json",
    ]


def clear_cache(suffix: str):
    for path in all_output_paths(suffix):
        if path.exists():
            path.unlink()
            logging.info(f"Deleted {path}")
    charts_dir = config.output_dir() / f"charts{suffix}"
    if charts_dir.exists():
        shutil.rmtree(charts_dir)
        logging.info(f"Deleted {charts_dir}/")
    screenshots_dir = config.output_dir() / "screenshots"
    if screenshots_dir.exists():
        shutil.rmtree(screenshots_dir)
        logging.info(f"Deleted {screenshots_dir}/")


def parse_stars(value: str) -> list[int]:
    """Parse comma-separated star ratings like '1', '1,2', '1,2,3'."""
    stars = []
    for part in value.split(","):
        s = int(part.strip())
        if s < 1 or s > 5:
            raise argparse.ArgumentTypeError(
                f"Star rating must be 1-5, got {s}"
            )
        stars.append(s)
    return sorted(set(stars))


# ── Pipeline step functions ────────────────────────────────────────────────


def step_scrape(args, logger):
    """Step 1: Scrape or load reviews."""
    if args.skip_scrape:
        import pandas as pd

        csv_path = config.output_dir() / "raw_reviews.csv"
        if not csv_path.exists():
            logger.error(f"{csv_path} not found. Cannot skip scraping without existing data.")
            sys.exit(1)
        reviews_df = pd.read_csv(csv_path, parse_dates=["date"])
        logger.info(f"Loaded {len(reviews_df)} Maya reviews from {csv_path}")

        gcash_path = config.output_dir() / "gcash_reviews.csv"
        if gcash_path.exists():
            gcash_df = pd.read_csv(gcash_path, parse_dates=["date"])
            logger.info(f"Loaded {len(gcash_df)} GCash reviews from {gcash_path}")
        else:
            logger.warning(f"{gcash_path} not found — competitor comparison will be skipped.")
            gcash_df = None
    else:
        reviews_df = scraper.run(months=args.months)
        gcash_df = scraper.run_gcash(months=args.months)

    return reviews_df, gcash_df


def step_filter_and_validate(args, reviews_df, logger):
    """Apply star filter and run data quality checks."""
    suffix = output_suffix(args.stars)

    if args.stars:
        import pandas as pd

        before = len(reviews_df)
        reviews_df = reviews_df[reviews_df["rating"].isin(args.stars)].reset_index(drop=True)
        star_label = ",".join(str(s) for s in args.stars)
        logger.info(f"Filtered to {star_label}-star reviews: {before} -> {len(reviews_df)}")

    logger.info(f"Total reviews for analysis: {len(reviews_df)}")

    if len(reviews_df) == 0:
        logger.error("No reviews match the filter. Cannot proceed.")
        sys.exit(1)

    quality = data_quality.run(reviews_df)
    if not quality["passed"]:
        logger.error("Data quality checks failed — cannot proceed.")
        sys.exit(1)

    return reviews_df, suffix


def step_temporal(reviews_df, suffix, logger):
    """Step 2: Temporal analysis."""
    return temporal_analyzer.run(reviews_df, suffix=suffix)


def step_comprehensive(reviews_df, suffix, logger):
    """Step 3: Comprehensive analysis."""
    return comprehensive_analyzer.run(reviews_df, suffix=suffix)


def step_competitor(reviews_df, gcash_df, suffix, logger):
    """Step 4: Competitor comparison."""
    if gcash_df is not None and len(gcash_df) > 0:
        return competitor_analysis.run(reviews_df, gcash_df, suffix=suffix)
    logger.warning("No GCash reviews available — skipping competitor comparison.")
    return None


def step_funnel(reviews_df, suffix, logger):
    """Step 4: Funnel analysis."""
    return funnel_analyzer.run(reviews_df, suffix=suffix)


def step_accessibility(reviews_df, suffix, logger):
    """Step 5: Accessibility & edge-case analysis."""
    return accessibility_analyzer.run(reviews_df, suffix=suffix)


def step_screenshots(logger):
    """Step 7: Download app screenshots."""
    return screenshot_scraper.run()


def step_insights(temporal_data, comprehensive_data, comparison, reviews_df,
                  suffix, logger, funnel_data=None, accessibility_data=None):
    """Step 8: Generate final insights report."""
    return insights_generator.run(
        temporal_data, comprehensive_data, suffix=suffix,
        comparison=comparison, reviews_df=reviews_df,
        funnel_data=funnel_data, accessibility_data=accessibility_data,
    )


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Maya Review Analysis Agent - UX insights from app reviews",
        epilog="Resume: Re-run the same command to resume from last checkpoint. "
               "Use --fresh to start over.",
    )
    parser.add_argument(
        "--months", type=int, default=12,
        help="Number of months of reviews to analyze (default: 12)",
    )
    parser.add_argument(
        "--stars", type=parse_stars, default=None,
        help="Filter by star rating: 1, 2, 3, 4, 5 or comma-separated (e.g. 1,2)",
    )
    parser.add_argument(
        "--skip-scrape", action="store_true",
        help="Skip scraping, use existing data/raw_reviews.csv",
    )
    parser.add_argument(
        "--backend", choices=["gemini", "ollama"], default="gemini",
        help="LLM backend: 'gemini' (cloud, needs API key) or 'ollama' (local, free)",
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help="Delete all cached data and re-run from scratch",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable DEBUG-level logging",
    )
    args = parser.parse_args()

    setup_logging(verbose=args.verbose)
    logger = logging.getLogger("main")

    llm.set_backend(args.backend)
    suffix = output_suffix(args.stars)

    if args.fresh:
        logger.info("Clearing cached data...")
        clear_cache(suffix)

    start_time = time.time()

    steps = [
        ("Scraping reviews", "Scraping reviews..."),
        ("Temporal analysis", "Running temporal analysis..."),
        ("Comprehensive analysis", "Running comprehensive analysis..."),
        ("Funnel analysis", "Running funnel analysis..."),
        ("Accessibility analysis", "Running accessibility analysis..."),
        ("Competitor comparison", "Running competitor comparison..."),
        ("Screenshot scraping", "Downloading app screenshots..."),
        ("Generating insights", "Generating final insights report..."),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        pipeline = progress.add_task("Pipeline", total=len(steps))

        # Step 1: Scrape
        progress.update(pipeline, description=steps[0][1])
        reviews_df, gcash_df = step_scrape(args, logger)
        reviews_df, suffix = step_filter_and_validate(args, reviews_df, logger)
        progress.advance(pipeline)

        # Step 2: Temporal
        progress.update(pipeline, description=steps[1][1])
        temporal_data = step_temporal(reviews_df, suffix, logger)
        progress.advance(pipeline)

        # Step 3: Comprehensive
        progress.update(pipeline, description=steps[2][1])
        comprehensive_data = step_comprehensive(reviews_df, suffix, logger)
        progress.advance(pipeline)

        # Step 4: Funnel analysis
        progress.update(pipeline, description=steps[3][1])
        funnel_data = step_funnel(reviews_df, suffix, logger)
        progress.advance(pipeline)

        # Step 5: Accessibility analysis
        progress.update(pipeline, description=steps[4][1])
        accessibility_data = step_accessibility(reviews_df, suffix, logger)
        progress.advance(pipeline)

        # Step 6: Competitor
        progress.update(pipeline, description=steps[5][1])
        comparison = step_competitor(reviews_df, gcash_df, suffix, logger)
        progress.advance(pipeline)

        # Step 7: Screenshots
        progress.update(pipeline, description=steps[6][1])
        screenshot_manifest = step_screenshots(logger)
        progress.advance(pipeline)

        # Step 8: Insights
        progress.update(pipeline, description=steps[7][1])
        insights = step_insights(
            temporal_data, comprehensive_data, comparison, reviews_df, suffix, logger,
            funnel_data=funnel_data, accessibility_data=accessibility_data,
        )
        progress.advance(pipeline)

    # ── Completion banner ──────────────────────────────────────────────
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    d = config.output_dir()
    table = Table(title="Output Files", show_header=True, header_style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("Path")
    table.add_row("Maya reviews", str(d / "raw_reviews.csv"))
    table.add_row("GCash reviews", str(d / "gcash_reviews.csv"))
    table.add_row("Temporal", str(d / f"temporal_analysis{suffix}.json"))
    table.add_row("Comprehensive", str(d / f"comprehensive_analysis{suffix}.json"))
    table.add_row("Funnel analysis", str(d / f"funnel_analysis{suffix}.json"))
    table.add_row("Accessibility", str(d / f"accessibility_analysis{suffix}.json"))
    table.add_row("Comparison", str(d / f"competitor_comparison{suffix}.json"))
    table.add_row("Screenshots", str(d / "screenshots/"))
    table.add_row("Journey map", str(d / f"journey_map{suffix}.json"))
    table.add_row("Insights", str(d / f"final_insights{suffix}.json"))
    table.add_row("Report", str(d / f"maya_insights_report{suffix}.md"))
    table.add_row("Charts", str(d / f"charts{suffix}/"))

    filter_line = ""
    if args.stars:
        filter_line = f"\nFilter: {','.join(str(s) for s in args.stars)}-star reviews only"

    panel = Panel(
        table,
        title=f"[bold green]COMPLETE[/bold green] in {minutes}m {seconds}s{filter_line}",
        border_style="green",
    )
    console.print(panel)


if __name__ == "__main__":
    main()
